"""表达式画布：SymPy → 自定义表达式树 → 分层着色 LaTeX → MathJax。"""

from __future__ import annotations

import html as html_lib
import json
import sys
from dataclasses import dataclass
from functools import partial

import sympy
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QObject, Qt, QTimer, QUrl, Signal, Slot
from PySide6.QtGui import QAction, QFont, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QSplitter,
    QStyle,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from expr_calculator.expr_tree import Add, Div, Eq, Expr, Integer, LatexPrinter, Mul, Point, Pow, Rational, Symbol, from_sympy, parse_sympy

BASE_DIR = Path(__file__).resolve().parent
MATHJAX_FILE = BASE_DIR.parent / "mathjax" / "es5" / "tex-svg.js"

PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<script>window.MathJax = {
  tex: {displayMath: [['$$', '$$']]},
  svg: {fontCache: 'local'},
  startup: {typeset: false}
};</script>
<script src="../mathjax/es5/tex-svg.js"></script>
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<style>
  html, body {margin: 0; padding: 0; height: 100%; background: #ffffff; overflow: hidden;}
  #canvas-wrap {
    position: absolute; inset: 0; overflow: auto; padding: 16px;
    box-sizing: border-box;
  }
  #canvas {
    position: relative; width: 2200px; height: 1400px;
    font-size: 42px;
    background-image: radial-gradient(#e6e9ee 1px, transparent 1px);
    background-size: 24px 24px;
  }
  #empty-hint {
    position: absolute; left: 40px; top: 40px; color: #8c959f;
    font: 14px/1.9 "Microsoft YaHei", sans-serif; pointer-events: none;
  }
  .math-item {
    position: absolute; box-sizing: border-box;
    padding: 16px 22px 34px; background: #ffffff;
    border: 1px solid #e5e7eb; border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  }
  .math-item.dragging {
    box-shadow: 0 10px 28px rgba(0, 0, 0, 0.16);
    border-color: #afb8c1;
  }
  .math-item.collision {
    border-color: #cf222e; background: #fff5f5;
  }
  .drag-handle {
    position: absolute; left: -11px; top: -11px;
    width: 24px; height: 24px; border-radius: 50%;
    border: 1.5px solid #e53935; background: #ffffff; color: #e53935;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; line-height: 1; cursor: grab; user-select: none;
    z-index: 10; opacity: 0.7;
  }
  .drag-handle:hover {opacity: 1; background: #fff5f5;}
  .math-item.dragging .drag-handle {cursor: grabbing;}
  .card-note {
    position: absolute; right: 10px; top: 8px; z-index: 11;
    padding: 1px 7px; border-radius: 999px;
    background: rgba(246, 248, 250, 0.94); border: 1px solid #e5e7eb;
    color: #57606a; font: 11px/1.6 "Microsoft YaHei", sans-serif;
    pointer-events: none; white-space: nowrap;
  }
  .card-actions {
    position: absolute; right: 6px; bottom: 6px; z-index: 12;
    display: flex; gap: 4px;
  }
  .card-button {
    border: 1px solid #d0d7de; border-radius: 5px;
    background: #f6f8fa; color: #57606a;
    font: 11px/1.4 "Microsoft YaHei", sans-serif;
    padding: 2px 7px; cursor: pointer; user-select: none;
    white-space: nowrap;
  }
  .card-button:hover {background: #eaeef2; color: #24292f;}
  .card-button.delete:hover {background: #ffebe9; border-color: #cf222e; color: #cf222e;}
  .math-item.selected {
    border-color: #0969da;
    box-shadow: 0 0 0 2px rgba(9, 105, 218, 0.22), 0 1px 3px rgba(0, 0, 0, 0.06);
  }
  .card-title {
    font: 11px/1.4 "Microsoft YaHei", sans-serif; color: #57606a;
    margin: 0 0 5px; max-width: 240px; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis; cursor: text;
  }
  .card-title:empty::before {content: "双击设置标题"; color: #c8ccd1;}
  .title-input {
    font: 11px "Microsoft YaHei", sans-serif; color: #1f2328;
    border: 1px solid #0969da; border-radius: 4px;
    padding: 0 4px; width: 150px; outline: none;
  }
  .math-item.collapsed {
    padding: 6px 12px; border-radius: 8px; box-shadow: none;
    background: #fbfcfd; font-size: 0.66em;
  }
  .math-item.collapsed .card-title {
    display: inline; margin: 0 10px 0 0; font-size: 10px;
    max-width: 160px; vertical-align: middle;
  }
  .math-item.collapsed .card-title:empty::before {content: none;}
  .math-item.collapsed .item-content {
    position: relative; display: inline-block; color: #1f2328;
    vertical-align: middle;
  }
  .math-item.collapsed .drag-handle {
    left: -9px; top: -9px; width: 18px; height: 18px;
    border-width: 1px; font-size: 11px;
  }
  .math-item.collapsed .card-note {
    position: static; display: inline-block; margin-left: 8px;
    vertical-align: middle; font-size: 10px; border-color: #e5e7eb;
  }
  .math-item.collapsed .card-actions {
    position: static; display: inline-flex; margin-left: 6px;
    vertical-align: middle;
  }
  .math-item.collapsed .card-actions .card-button {display: none;}
  .math-item.collapsed .card-actions .card-button.collapse {
    display: inline-block; padding: 0 5px; border: none;
    background: transparent; color: #8c959f; font-size: 10px;
  }
  .math-item.collapsed .card-actions .card-button.collapse:hover {
    background: #eaeef2; color: #24292f;
  }
  .math-item.collapsed svg,
  .math-item.collapsed g[id*="__l0-"],
  .math-item.collapsed g[id*="__l1-"],
  .math-item.collapsed g[id*="__l2-"],
  .math-item.collapsed g[id*="__l3-"] {color: #1f2328;}
  .item-content {position: relative; color: #1f2328; display: inline-block;}
  .item-content.error {
    color: #cf222e; font: 14px/1.6 "Microsoft YaHei", sans-serif;
    white-space: pre-wrap; max-width: 520px;
  }
  .action-layer {
    position: absolute; inset: 0; z-index: 6; pointer-events: none;
  }
  .action-hit {position: absolute; pointer-events: auto; cursor: pointer;}
  svg {color: #1f2328;}
  g[id*="__l0-"] {color: #e53935;}
  g[id*="__l1-"] {color: #2e7d32;}
  g[id*="__l2-"] {color: #1565c0;}
  g[id*="__l3-"] {color: #6a1b9a;}
  g[id*="__l"] {cursor: pointer;}
  #toolbar {
    position: fixed; top: 10px; right: 14px; z-index: 15;
    display: flex; align-items: center; gap: 8px;
    padding: 4px 12px; border-radius: 999px;
    background: rgba(255, 255, 255, 0.94);
    border: 1px solid #d0d7de; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
    font: 12px "Microsoft YaHei", sans-serif; color: #57606a;
    user-select: none;
  }
  #size-slider {width: 120px; accent-color: #0969da;}
  #selection-box {
    position: fixed; display: none; pointer-events: none; z-index: 20;
    border: 1.5px dashed #0969da; border-radius: 6px;
    box-sizing: border-box;
  }
  #selection-tag {
    position: fixed; display: none; pointer-events: none; z-index: 21;
    padding: 2px 7px; border-radius: 4px; background: #ffffff;
    border: 1px solid currentColor;
    font: 12px/1.4 "Microsoft YaHei", sans-serif;
    white-space: nowrap;
  }
  #node-handle {
    position: fixed; display: none; width: 20px; height: 20px;
    border-radius: 50%; background: #ffffff; border: 1.5px solid #0969da;
    color: #0969da; align-items: center; justify-content: center;
    font-size: 12px; line-height: 1; cursor: grab; z-index: 25;
    user-select: none; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  }
  #node-handle:hover {background: #f0f7ff;}
  #transform-button {
    position: fixed; display: none; width: 20px; height: 20px;
    border-radius: 50%; background: #ffffff; border: 1.5px solid #0969da;
    color: #0969da; align-items: center; justify-content: center;
    font-size: 11px; line-height: 1; cursor: pointer; z-index: 25;
    user-select: none; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  }
  #transform-button:hover {background: #f0f7ff;}
  #action-badge {
    position: fixed; display: none; z-index: 30;
    padding: 3px 9px; border-radius: 999px;
    background: #24292f; color: #ffffff;
    font: 12px/1.4 "Microsoft YaHei", sans-serif;
    cursor: pointer; user-select: none; white-space: nowrap;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.18);
  }
  #action-badge:hover {background: #0969da;}
</style>
</head>
<body>
<div id="canvas-wrap">
  <div id="canvas">
    <div id="empty-hint">在上方输入表达式，按回车或点击“添加”<br>可向画布添加多个表达式；拖拽左上角红圈移动。</div>
  </div>
</div>
<div id="toolbar">
  <span>字号</span>
  <input id="size-slider" type="range" min="24" max="96" step="2" value="42">
  <span id="size-value">42px</span>
</div>
<div id="selection-box"></div>
<div id="selection-tag"></div>
<div id="node-handle" title="拖拽选中节点">⠿</div>
<div id="transform-button" title="变形选中节点">变</div>
<div id="action-badge"></div>
<script>
const canvas = document.getElementById('canvas');
const badge = document.getElementById('action-badge');
const SVG_NS = 'http://www.w3.org/2000/svg';

let nodeMeta = {};
let selectedId = null;
let hoverNode = null;
let hoverRect = null;
let actionTarget = null;
let dragState = null;
let nodeDrag = null;
let suppressClickUntil = 0;
let typesetQueue = Promise.resolve();

function registerMeta(itemId, meta) {
  const prefix = itemId + '__';
  for (const key of Object.keys(nodeMeta)) {
    if (key.indexOf(prefix) === 0) delete nodeMeta[key];
  }
  if (meta) Object.assign(nodeMeta, meta);
}

function unregisterMeta(itemId) {
  const prefix = itemId + '__';
  for (const key of Object.keys(nodeMeta)) {
    if (key.indexOf(prefix) === 0) delete nodeMeta[key];
  }
}

function colorToRgba(color, alpha) {
  const m = color.match(/\\d+/g);
  if (!m || m.length < 3) return 'rgba(9,105,218,' + alpha + ')';
  return 'rgba(' + m[0] + ',' + m[1] + ',' + m[2] + ',' + alpha + ')';
}

function hideSelection() {
  document.getElementById('selection-box').style.display = 'none';
  document.getElementById('selection-tag').style.display = 'none';
  document.getElementById('node-handle').style.display = 'none';
  document.getElementById('transform-button').style.display = 'none';
}

function clearSelection(notify) {
  selectedId = null;
  hideSelection();
  canvas.querySelectorAll('.math-item.selected').forEach(function (el) {
    el.classList.remove('selected');
  });
  if (notify && window.bridge && window.bridge.clear) {
    try { window.bridge.clear(); } catch (err) {}
  }
}

function installHitAreas(item) {
  if (item.classList.contains('collapsed')) return;
  const svg = item.querySelector('svg');
  if (!svg) return;
  const viewBox = svg.viewBox.baseVal;
  const svgRect = svg.getBoundingClientRect();
  const unitsPerPx = (viewBox && svgRect.width) ? viewBox.width / svgRect.width : 1;
  item.__unitsPerPx = unitsPerPx;
  const pad = 5 * unitsPerPx;
  const groups = Array.from(item.querySelectorAll('g[id]')).filter(function (group) {
    return group.id.indexOf('__l') >= 0;
  });
  const boxes = [];
  for (const group of groups) {
    let box = null;
    try { box = group.getBBox(); } catch (err) { box = null; }
    boxes.push([group, box]);
  }
  for (const [group, box] of boxes) {
    if (!box || !isFinite(box.width) || !isFinite(box.height)) continue;
    if (box.width <= 0 || box.height <= 0) continue;
    const area = {
      x: box.x - pad, y: box.y - pad,
      width: box.width + 2 * pad, height: box.height + 2 * pad
    };
    group.__hitBox = area;
    group.__padPx = 5;
    group.__unitsPerPx = unitsPerPx;
    const rect = document.createElementNS(SVG_NS, 'rect');
    rect.setAttribute('class', 'hit-area');
    rect.setAttribute('x', area.x);
    rect.setAttribute('y', area.y);
    rect.setAttribute('width', area.width);
    rect.setAttribute('height', area.height);
    rect.setAttribute('fill', 'transparent');
    rect.setAttribute('pointer-events', 'all');
    group.insertBefore(rect, group.firstChild);
  }
}

function setHover(group) {
  if (group === hoverNode) return;
  if (!group || !group.__hitBox) {
    if (hoverRect) hoverRect.remove();
    hoverNode = null;
    return;
  }
  if (!hoverRect) {
    hoverRect = document.createElementNS(SVG_NS, 'rect');
    hoverRect.setAttribute('fill', '#000000');
    hoverRect.setAttribute('fill-opacity', '0.08');
    hoverRect.setAttribute('pointer-events', 'none');
  }
  const area = group.__hitBox;
  hoverRect.setAttribute('x', area.x);
  hoverRect.setAttribute('y', area.y);
  hoverRect.setAttribute('width', area.width);
  hoverRect.setAttribute('height', area.height);
  hoverRect.setAttribute('rx', 4 * (group.__unitsPerPx || 1));
  const first = group.firstChild;
  const anchor = (first && first.classList && first.classList.contains('hit-area'))
    ? first.nextSibling : first;
  group.insertBefore(hoverRect, anchor);
  hoverNode = group;
}

function actionForMo(mo) {
  if (!mo) return null;
  const item = mo.closest('.math-item');
  if (!item) return null;
  const addGroup = mo.closest('g[id*="__l"]');
  const meta = addGroup ? nodeMeta[addGroup.id] : null;
  if (meta && meta.type === 'Add') {
    const use = mo.querySelector('use');
    const code = use ? use.getAttribute('data-c') : null;
    if (code === '2B' || code === '2212') {
      const operators = Array.from(addGroup.querySelectorAll('g[data-mml-node="mo"]')).filter(function (node) {
        if (node.closest('g[id*="__l"]') !== addGroup) return false;
        const glyph = node.querySelector('use');
        const value = glyph ? glyph.getAttribute('data-c') : null;
        return value === '2B' || value === '2212';
      });
      const index = operators.indexOf(mo);
      if (index >= 0) {
        return {kind: 'swap', id: addGroup.id, index: index, item: item.dataset.id};
      }
    }
  }
  const wrapper = mo.parentElement;
  if (wrapper) {
    const inner = wrapper.querySelector(':scope > g[id*="__l"]');
    const innerMeta = inner ? nodeMeta[inner.id] : null;
    if (innerMeta && innerMeta.type === 'Add' && innerMeta.expandable) {
      return {kind: 'expand', id: inner.id, index: -1, item: item.dataset.id};
    }
  }
  return null;
}

function installActionAreas(item) {
  if (item.classList.contains('collapsed')) return;
  const layer = item.querySelector('.action-layer');
  if (!layer) return;
  layer.textContent = '';
  const layerRect = layer.getBoundingClientRect();
  const pad = 8;
  const mos = Array.from(item.querySelectorAll('g[data-mml-node="mo"]'));
  const items = [];
  for (const mo of mos) {
    const action = actionForMo(mo);
    if (!action) continue;
    const rect = mo.getBoundingClientRect();
    if (!rect || rect.width <= 0 || rect.height <= 0) continue;
    items.push([action, rect]);
  }
  for (const [action, rect] of items) {
    const hit = document.createElement('div');
    hit.className = 'action-hit';
    hit.dataset.action = action.kind;
    hit.dataset.item = action.item;
    hit.dataset.node = action.id;
    hit.dataset.index = action.index;
    hit.style.left = (rect.left - layerRect.left - pad) + 'px';
    hit.style.top = (rect.top - layerRect.top - pad) + 'px';
    hit.style.width = (rect.width + 2 * pad) + 'px';
    hit.style.height = (rect.height + 2 * pad) + 'px';
    layer.appendChild(hit);
  }
}

function interactiveAt(target) {
  if (!target || !target.closest) return null;
  const hit = target.closest('.action-hit');
  if (hit) {
    return {
      kind: hit.dataset.action,
      id: hit.dataset.node,
      item: hit.dataset.item,
      index: Number(hit.dataset.index),
      rect: hit.getBoundingClientRect()
    };
  }
  const mo = target.closest('g[data-mml-node="mo"]');
  if (!mo || !mo.closest('.math-item')) return null;
  const action = actionForMo(mo);
  if (!action) return null;
  action.rect = mo.getBoundingClientRect();
  return action;
}

function showBadge(action) {
  actionTarget = action;
  badge.textContent = action.kind === 'swap' ? '⇄ 交换' : '⤢ 展开';
  badge.style.display = 'block';
  const rect = action.rect;
  const width = badge.offsetWidth;
  const height = badge.offsetHeight;
  let left = rect.left + rect.width / 2 - width / 2;
  left = Math.max(4, Math.min(left, window.innerWidth - width - 4));
  let top = rect.top - height - 6;
  if (top < 4) top = rect.bottom + 6;
  badge.style.left = left + 'px';
  badge.style.top = top + 'px';
}

function hideBadge() {
  actionTarget = null;
  badge.style.display = 'none';
}

function performAction(action) {
  if (window.bridge) {
    try {
      if (action.kind === 'swap' && window.bridge.swap) {
        window.bridge.swap(action.item, action.id, action.index);
      } else if (action.kind === 'expand' && window.bridge.expand) {
        window.bridge.expand(action.item, action.id);
      }
    } catch (err) {}
  }
  hideBadge();
}

function selectNode(group) {
  const id = group.id;
  const item = group.closest('.math-item');
  const meta = nodeMeta[id] || {};
  const padPx = group.__padPx || 0;
  const raw = group.getBoundingClientRect();
  const rect = {
    left: raw.left + padPx, top: raw.top + padPx,
    width: raw.width - 2 * padPx, height: raw.height - 2 * padPx
  };
  rect.right = rect.left + rect.width;
  rect.bottom = rect.top + rect.height;
  const color = getComputedStyle(group).color || '#0969da';
  const box = document.getElementById('selection-box');
  const tag = document.getElementById('selection-tag');
  box.style.display = 'block';
  box.style.left = (rect.left - 5) + 'px';
  box.style.top = (rect.top - 5) + 'px';
  box.style.width = (rect.width + 10) + 'px';
  box.style.height = (rect.height + 10) + 'px';
  box.style.borderColor = color;
  box.style.background = colorToRgba(color, 0.08);
  tag.style.display = 'block';
  tag.style.color = color;
  tag.textContent = (meta.type || '节点') + ' · 第 ' + (meta.depth === undefined ? '?' : meta.depth) + ' 层';
  const above = rect.top - 28;
  tag.style.left = Math.max(4, rect.left) + 'px';
  tag.style.top = (above > 4 ? above : rect.bottom + 8) + 'px';
  const nodeHandle = document.getElementById('node-handle');
  nodeHandle.style.display = 'flex';
  nodeHandle.style.left = (rect.left - 10) + 'px';
  nodeHandle.style.top = (rect.top - 10) + 'px';
  nodeHandle.style.borderColor = color;
  nodeHandle.style.color = color;
  const transformButton = document.getElementById('transform-button');
  transformButton.style.display = 'flex';
  transformButton.style.left = (rect.right - 10) + 'px';
  transformButton.style.top = (rect.bottom - 10) + 'px';
  transformButton.style.borderColor = color;
  transformButton.style.color = color;
  selectedId = id;
  canvas.querySelectorAll('.math-item').forEach(function (el) {
    el.classList.toggle('selected', el === item);
  });
  if (window.bridge && window.bridge.select) {
    try { window.bridge.select(item ? item.dataset.id : '', id); } catch (err) {}
  }
}

function selectById(id) {
  const group = document.getElementById(id);
  if (group) selectNode(group);
}

function buildGhost(group, svg, svgRect) {
  const wrapper = document.createElement('div');
  wrapper.style.position = 'fixed';
  wrapper.style.left = svgRect.left + 'px';
  wrapper.style.top = svgRect.top + 'px';
  wrapper.style.width = svgRect.width + 'px';
  wrapper.style.height = svgRect.height + 'px';
  wrapper.style.pointerEvents = 'none';
  wrapper.style.zIndex = '40';
  wrapper.style.opacity = '0.8';
  const cloneSvg = document.createElementNS(SVG_NS, 'svg');
  cloneSvg.setAttribute('viewBox', '0 0 ' + svgRect.width + ' ' + svgRect.height);
  cloneSvg.setAttribute('width', svgRect.width);
  cloneSvg.setAttribute('height', svgRect.height);
  cloneSvg.setAttribute('fill', 'currentColor');
  cloneSvg.style.overflow = 'visible';
  const holder = document.createElementNS(SVG_NS, 'g');
  const parent = group.parentElement;
  const ctm = parent ? parent.getCTM() : null;
  if (ctm) {
    holder.setAttribute('transform', 'matrix(' + [ctm.a, ctm.b, ctm.c, ctm.d, ctm.e, ctm.f].join(',') + ')');
  }
  const clone = group.cloneNode(true);
  const sourceGroups = [group].concat(Array.from(group.querySelectorAll('g[id]')));
  const cloneGroups = [clone].concat(Array.from(clone.querySelectorAll('g[id]')));
  for (let i = 0; i < sourceGroups.length; i += 1) {
    const source = sourceGroups[i];
    const target = cloneGroups[i];
    if (!target) continue;
    try { target.style.color = getComputedStyle(source).color; } catch (err) {}
    if (target.id) target.removeAttribute('id');
  }
  clone.querySelectorAll('.hit-area').forEach(function (rect) { rect.remove(); });
  holder.appendChild(clone);
  cloneSvg.appendChild(holder);
  wrapper.appendChild(cloneSvg);
  return wrapper;
}

function startNodeDrag(event) {
  if (event.button !== 0 || !selectedId) return;
  const group = document.getElementById(selectedId);
  if (!group) return;
  const item = group.closest('.math-item');
  const svg = group.closest('svg');
  if (!item || !svg) return;
  event.preventDefault();
  event.stopPropagation();
  setHover(null);
  hideBadge();
  const svgRect = svg.getBoundingClientRect();
  const nodeRect = group.getBoundingClientRect();
  const ghost = buildGhost(group, svg, svgRect);
  document.body.appendChild(ghost);
  nodeDrag = {
    pointerId: event.pointerId,
    startX: event.clientX,
    startY: event.clientY,
    dx: 0,
    dy: 0,
    moved: false,
    groupRect: nodeRect,
    ghost: ghost,
    ghostBaseLeft: svgRect.left,
    ghostBaseTop: svgRect.top,
    itemId: item.dataset.id,
    nodeId: selectedId
  };
  try { event.currentTarget.setPointerCapture(event.pointerId); } catch (err) {}
}

function moveNodeDrag(event) {
  if (!nodeDrag) return;
  const dx = event.clientX - nodeDrag.startX;
  const dy = event.clientY - nodeDrag.startY;
  nodeDrag.dx = dx;
  nodeDrag.dy = dy;
  if (Math.abs(dx) + Math.abs(dy) > 3) nodeDrag.moved = true;
  nodeDrag.ghost.style.left = (nodeDrag.ghostBaseLeft + dx) + 'px';
  nodeDrag.ghost.style.top = (nodeDrag.ghostBaseTop + dy) + 'px';
}

function endNodeDrag(event) {
  if (!nodeDrag) return;
  const state = nodeDrag;
  nodeDrag = null;
  state.ghost.remove();
  try { event.currentTarget.releasePointerCapture(state.pointerId); } catch (err) {}
  if (!state.moved) return;
  suppressClickUntil = Date.now() + 300;
  const rect = {
    left: state.groupRect.left + state.dx,
    top: state.groupRect.top + state.dy,
    right: state.groupRect.right + state.dx,
    bottom: state.groupRect.bottom + state.dy
  };
  let target = null;
  let bestArea = 0;
  for (const item of canvas.querySelectorAll('.math-item')) {
    const r = item.getBoundingClientRect();
    const width = Math.min(rect.right, r.right) - Math.max(rect.left, r.left);
    const height = Math.min(rect.bottom, r.bottom) - Math.max(rect.top, r.top);
    if (width > 0 && height > 0) {
      const area = width * height;
      if (area > bestArea) {
        bestArea = area;
        target = item;
      }
    }
  }
  if (target && window.bridge && window.bridge.dropNode) {
    try { window.bridge.dropNode(state.itemId, state.nodeId, target.dataset.id); } catch (err) {}
    return;
  }
  if (!target && window.bridge && window.bridge.dropNodeOnCanvas) {
    const canvasRect = canvas.getBoundingClientRect();
    const x = Math.max(24, rect.left - canvasRect.left);
    const y = Math.max(24, rect.top - canvasRect.top);
    try { window.bridge.dropNodeOnCanvas(state.itemId, state.nodeId, x, y); } catch (err) {}
  }
}

function updateEmptyHint() {
  const hint = document.getElementById('empty-hint');
  if (!hint) return;
  hint.style.display = canvas.querySelector('.math-item') ? 'none' : 'block';
}

function overlapArea(a, b, gap) {
  const width = Math.min(a.right + gap, b.right) - Math.max(a.left - gap, b.left);
  const height = Math.min(a.bottom + gap, b.bottom) - Math.max(a.top - gap, b.top);
  return (width > 0 && height > 0) ? width * height : 0;
}

function overlappingItems(rect, item, gap) {
  const result = [];
  for (const other of canvas.querySelectorAll('.math-item')) {
    if (other === item) continue;
    const area = overlapArea(rect, other.getBoundingClientRect(), gap);
    if (area > 0) result.push({item: other, area: area});
  }
  result.sort(function (a, b) { return b.area - a.area; });
  return result;
}

function itemsOverlap(rect, item, gap) {
  return overlappingItems(rect, item, gap).length > 0;
}

function findFreeSpot(item) {
  const width = item.offsetWidth;
  const height = item.offsetHeight;
  const maxX = Math.max(24, canvas.clientWidth - width - 24);
  const maxY = Math.max(24, canvas.clientHeight - height - 24);
  for (let y = 24; y <= maxY; y += 40) {
    for (let x = 24; x <= maxX; x += 40) {
      item.style.left = x + 'px';
      item.style.top = y + 'px';
      if (!itemsOverlap(item.getBoundingClientRect(), item, 12)) return {x: x, y: y};
    }
  }
  return {x: 24, y: 24};
}

function createItemElement(data) {
  const item = document.createElement('div');
  item.className = 'math-item';
  item.dataset.id = data.id;
  item.dataset.kind = data.kind || 'expression';

  const handle = document.createElement('div');
  handle.className = 'drag-handle';
  handle.textContent = '⠿';
  handle.title = '拖拽移动（第 0 层）';
  handle.addEventListener('pointerdown', startDrag);
  handle.addEventListener('pointermove', moveDrag);
  handle.addEventListener('pointerup', endDrag);
  handle.addEventListener('pointercancel', endDrag);
  handle.addEventListener('click', function (event) { event.stopPropagation(); });

  const title = document.createElement('div');
  title.className = 'card-title';
  title.textContent = data.title || '';
  title.title = '双击编辑标题';
  title.addEventListener('dblclick', function (event) {
    event.preventDefault();
    event.stopPropagation();
    startTitleEdit(item);
  });

  const content = document.createElement('div');
  content.className = 'item-content';
  content.textContent = '$$' + data.latex + '$$';

  const layer = document.createElement('div');
  layer.className = 'action-layer';

  const actions = document.createElement('div');
  actions.className = 'card-actions';
  const copyButton = document.createElement('button');
  copyButton.type = 'button';
  copyButton.className = 'card-button';
  copyButton.textContent = '复制';
  copyButton.title = '复制这张卡片';
  copyButton.addEventListener('click', function (event) {
    event.preventDefault();
    event.stopPropagation();
    if (window.bridge && window.bridge.copyItem) {
      try { window.bridge.copyItem(item.dataset.id); } catch (err) {}
    }
  });
  const deleteButton = document.createElement('button');
  deleteButton.type = 'button';
  deleteButton.className = 'card-button delete';
  deleteButton.textContent = '删除';
  deleteButton.title = '删除这张卡片';
  deleteButton.addEventListener('click', function (event) {
    event.preventDefault();
    event.stopPropagation();
    if (window.bridge && window.bridge.deleteItem) {
      try { window.bridge.deleteItem(item.dataset.id); } catch (err) {}
    }
  });
  const collapseButton = document.createElement('button');
  collapseButton.type = 'button';
  collapseButton.className = 'card-button collapse';
  collapseButton.textContent = '折叠';
  collapseButton.title = '折叠或展开这张卡片';
  collapseButton.addEventListener('click', function (event) {
    event.preventDefault();
    event.stopPropagation();
    toggleCollapse(item);
  });
  actions.append(copyButton, deleteButton, collapseButton);

  item.dataset.source = data.latex || '';
  item.dataset.plain = data.plain || '';
  item.append(handle, title, content, layer);
  if (data.note) {
    const note = document.createElement('div');
    note.className = 'card-note';
    note.textContent = data.note;
    item.appendChild(note);
  }
  item.appendChild(actions);
  if (data.collapsed) setCollapsed(item, true);
  item.addEventListener('click', function (event) {
    if (Date.now() < suppressClickUntil) return;
    if (event.target.closest('g[id]')) return;
    if (event.target.closest('.card-button, .card-title, .drag-handle, .title-input')) return;
    if (window.bridge && window.bridge.selectCard) {
      try { window.bridge.selectCard(item.dataset.id); } catch (err) {}
    }
  });
  return item;
}

function startTitleEdit(item) {
  const title = item.querySelector('.card-title');
  if (!title || title.querySelector('input')) return;
  const previous = title.textContent || '';
  const input = document.createElement('input');
  input.className = 'title-input';
  input.type = 'text';
  input.value = previous;
  title.textContent = '';
  title.appendChild(input);
  input.focus();
  input.select();
  let done = false;
  const finish = function (save) {
    if (done) return;
    done = true;
    const text = save ? input.value.trim() : previous;
    title.textContent = text;
    if (save && window.bridge && window.bridge.setTitle) {
      try { window.bridge.setTitle(item.dataset.id, text); } catch (err) {}
    }
  };
  input.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') { event.preventDefault(); finish(true); }
    else if (event.key === 'Escape') { event.preventDefault(); finish(false); }
  });
  input.addEventListener('blur', function () { finish(true); });
  input.addEventListener('click', function (event) { event.stopPropagation(); });
  input.addEventListener('dblclick', function (event) { event.stopPropagation(); });
}

function selectCardById(itemId) {
  clearSelection(false);
  canvas.querySelectorAll('.math-item').forEach(function (el) {
    el.classList.toggle('selected', el.dataset.id === itemId);
  });
}

function setCollapsed(item, collapsed) {
  item.classList.toggle('collapsed', collapsed);
  const button = item.querySelector('.card-button.collapse');
  if (button) button.textContent = collapsed ? '展开' : '折叠';
}

async function toggleCollapse(item) {
  const collapsed = !item.classList.contains('collapsed');
  const content = item.querySelector('.item-content');
  if (collapsed) {
    clearSelection(false);
    setHover(null);
    hideBadge();
    item.querySelectorAll('.hit-area').forEach(function (rect) { rect.remove(); });
    const layer = item.querySelector('.action-layer');
    if (layer) layer.textContent = '';
  }
  setCollapsed(item, collapsed);
  content.textContent = '$$' + (item.dataset.source || '') + '$$';
  try {
    await queueTypeset(item);
    if (!collapsed) {
      installHitAreas(item);
      installActionAreas(item);
    }
  } catch (err) {
    content.classList.add('error');
    content.textContent = String(err);
  }
  if (window.bridge && window.bridge.setCollapsed) {
    try { window.bridge.setCollapsed(item.dataset.id, collapsed); } catch (err) {}
  }
}

function typesetItem(item) {
  const content = item.querySelector('.item-content');
  return MathJax.startup.promise.then(function () {
    return MathJax.typesetPromise([content]);
  });
}

function queueTypeset(item) {
  const task = function () { return typesetItem(item); };
  typesetQueue = typesetQueue.then(task, task);
  return typesetQueue;
}

async function addItem(data) {
  const item = createItemElement(data);
  const pinned = typeof data.x === 'number' && typeof data.y === 'number';
  const startX = pinned ? data.x : 24;
  const startY = pinned ? data.y : 24;
  item.style.left = startX + 'px';
  item.style.top = startY + 'px';
  canvas.appendChild(item);
  registerMeta(data.id, data.meta);
  try {
    await queueTypeset(item);
    installHitAreas(item);
    installActionAreas(item);
  } catch (err) {
    const content = item.querySelector('.item-content');
    content.classList.add('error');
    content.textContent = String(err);
  }
  const pos = pinned ? {x: startX, y: startY} : findFreeSpot(item);
  updateEmptyHint();
  try { item.scrollIntoView({block: 'nearest', inline: 'nearest'}); } catch (err) {}
  if (window.bridge && window.bridge.placeItem) {
    try { window.bridge.placeItem(data.id, pos.x, pos.y); } catch (err) {}
  }
}

async function updateItem(itemId, source, meta, selectId, kind, note, plain) {
  const item = Array.from(canvas.querySelectorAll('.math-item')).find(function (el) {
    return el.dataset.id === itemId;
  });
  if (!item) return;
  clearSelection(false);
  setHover(null);
  hideBadge();
  registerMeta(itemId, meta);
  item.dataset.kind = kind || 'expression';
  let noteElement = item.querySelector('.card-note');
  if (note) {
    if (!noteElement) {
      noteElement = document.createElement('div');
      noteElement.className = 'card-note';
      const actions = item.querySelector('.card-actions');
      if (actions) {
        item.insertBefore(noteElement, actions);
      } else {
        item.appendChild(noteElement);
      }
    }
    noteElement.textContent = note;
  } else if (noteElement) {
    noteElement.remove();
  }
  item.dataset.source = source;
  item.dataset.plain = plain || '';
  const content = item.querySelector('.item-content');
  content.classList.remove('error');
  content.textContent = '$$' + source + '$$';
  try {
    await queueTypeset(item);
    item.querySelectorAll('.hit-area').forEach(function (rect) { rect.remove(); });
    installHitAreas(item);
    installActionAreas(item);
    if (selectId) selectById(selectId);
  } catch (err) {
    content.classList.add('error');
    content.textContent = String(err);
  }
}

async function setCanvas(items) {
  clearCanvas();
  for (const data of items) {
    const item = createItemElement(data);
    item.style.left = (data.x || 0) + 'px';
    item.style.top = (data.y || 0) + 'px';
    canvas.appendChild(item);
    registerMeta(data.id, data.meta);
    try {
      await queueTypeset(item);
      installHitAreas(item);
      installActionAreas(item);
    } catch (err) {
      const content = item.querySelector('.item-content');
      content.classList.add('error');
      content.textContent = String(err);
    }
  }
  updateEmptyHint();
}

function clearCanvas() {
  clearSelection(false);
  setHover(null);
  hideBadge();
  canvas.querySelectorAll('.math-item').forEach(function (item) { item.remove(); });
  nodeMeta = {};
  updateEmptyHint();
}

function removeItem(itemId) {
  const item = Array.from(canvas.querySelectorAll('.math-item')).find(function (el) {
    return el.dataset.id === itemId;
  });
  if (!item) return;
  if (selectedId && selectedId.indexOf(itemId + '__') === 0) clearSelection(false);
  unregisterMeta(itemId);
  item.remove();
  updateEmptyHint();
}

function startDrag(event) {
  if (event.button !== 0) return;
  const item = event.currentTarget.closest('.math-item');
  if (!item) return;
  event.preventDefault();
  event.stopPropagation();
  dragState = {
    item: item,
    pointerId: event.pointerId,
    startX: event.clientX,
    startY: event.clientY,
    originLeft: parseFloat(item.style.left) || 0,
    originTop: parseFloat(item.style.top) || 0,
    moved: false
  };
  item.classList.add('dragging');
  item.style.zIndex = 9;
  try { event.currentTarget.setPointerCapture(event.pointerId); } catch (err) {}
  clearSelection(false);
  setHover(null);
  hideBadge();
}

function moveDrag(event) {
  if (!dragState) return;
  const dx = event.clientX - dragState.startX;
  const dy = event.clientY - dragState.startY;
  if (Math.abs(dx) + Math.abs(dy) > 3) dragState.moved = true;
  const item = dragState.item;
  let left = dragState.originLeft + dx;
  let top = dragState.originTop + dy;
  left = Math.max(0, Math.min(left, canvas.clientWidth - item.offsetWidth));
  top = Math.max(0, Math.min(top, canvas.clientHeight - item.offsetHeight));
  item.style.left = left + 'px';
  item.style.top = top + 'px';
}

function endDrag(event) {
  if (!dragState) return;
  const state = dragState;
  dragState = null;
  const item = state.item;
  item.classList.remove('dragging');
  item.style.zIndex = '';
  try { event.currentTarget.releasePointerCapture(state.pointerId); } catch (err) {}
  if (!state.moved) return;
  suppressClickUntil = Date.now() + 300;
  const rect = item.getBoundingClientRect();
  const overlaps = overlappingItems(rect, item, 8);
  if (overlaps.length > 0) {
    item.style.left = state.originLeft + 'px';
    item.style.top = state.originTop + 'px';
    item.classList.add('collision');
    setTimeout(function () { item.classList.remove('collision'); }, 450);
    const equationPair = overlaps.find(function (entry) {
      return item.dataset.kind === 'equation' && entry.item.dataset.kind === 'equation';
    });
    if (equationPair && window.bridge && window.bridge.openSystem) {
      try {
        window.bridge.openSystem(item.dataset.id, equationPair.item.dataset.id);
      } catch (err) {}
      return;
    }
    const expressionPair = overlaps.find(function (entry) {
      return item.dataset.kind === 'expression' && entry.item.dataset.kind === 'expression';
    });
    if (expressionPair && window.bridge && window.bridge.openExpressionPair) {
      try {
        window.bridge.openExpressionPair(item.dataset.id, expressionPair.item.dataset.id);
      } catch (err) {}
    }
    return;
  }
  if (window.bridge && window.bridge.moveItem) {
    try {
      window.bridge.moveItem(
        item.dataset.id,
        parseFloat(item.style.left) || 0,
        parseFloat(item.style.top) || 0
      );
    } catch (err) {}
  }
}

document.addEventListener('click', function (event) {
  if (Date.now() < suppressClickUntil) return;
  if (badge.contains(event.target)) return;
  if (event.target.closest && event.target.closest('#toolbar')) return;
  const action = interactiveAt(event.target);
  if (action) {
    performAction(action);
    return;
  }
  const target = event.target;
  const group = target && target.closest ? target.closest('g[id*="__l"]') : null;
  if (group) {
    selectNode(group);
  } else if (!(target && target.closest && target.closest('.math-item'))) {
    clearSelection(true);
  }
});
document.addEventListener('mousemove', function (event) {
  if (dragState || nodeDrag) return;
  if (badge.contains(event.target)) return;
  const action = interactiveAt(event.target);
  if (action) {
    const group = document.getElementById(action.id);
    if (group) setHover(group);
    showBadge(action);
    return;
  }
  hideBadge();
  const target = event.target;
  const group = target && target.closest ? target.closest('g[id*="__l"]') : null;
  setHover(group);
});
document.addEventListener('mouseout', function (event) {
  if (!event.relatedTarget) {
    setHover(null);
    hideBadge();
  }
});
window.addEventListener('scroll', function () {
  hideSelection();
  hideBadge();
}, true);
window.addEventListener('resize', function () {
  if (selectedId) selectById(selectedId);
});
badge.addEventListener('click', function (event) {
  event.stopPropagation();
  if (actionTarget) performAction(actionTarget);
});
const transformButton = document.getElementById('transform-button');
transformButton.addEventListener('click', function (event) {
  event.stopPropagation();
  if (!selectedId) return;
  const group = document.getElementById(selectedId);
  const item = group ? group.closest('.math-item') : null;
  if (item && window.bridge && window.bridge.transform) {
    try { window.bridge.transform(item.dataset.id, selectedId); } catch (err) {}
  }
});
const nodeHandle = document.getElementById('node-handle');
nodeHandle.addEventListener('pointerdown', startNodeDrag);
nodeHandle.addEventListener('pointermove', moveNodeDrag);
nodeHandle.addEventListener('pointerup', endNodeDrag);
nodeHandle.addEventListener('pointercancel', endNodeDrag);
nodeHandle.addEventListener('click', function (event) { event.stopPropagation(); });

function setupBridge() {
  if (window.QWebChannel && window.qt && qt.webChannelTransport) {
    new QWebChannel(qt.webChannelTransport, function (channel) {
      window.bridge = channel.objects.bridge;
    });
  }
}

function refreshHitAreas() {
  hideBadge();
  setHover(null);
  canvas.querySelectorAll('.math-item').forEach(function (item) {
    item.querySelectorAll('.hit-area').forEach(function (rect) { rect.remove(); });
    installHitAreas(item);
    installActionAreas(item);
  });
  if (selectedId) selectById(selectedId);
}

const sizeSlider = document.getElementById('size-slider');
const sizeValue = document.getElementById('size-value');
sizeSlider.addEventListener('input', function () {
  const px = Number(sizeSlider.value);
  sizeValue.textContent = px + 'px';
  canvas.style.fontSize = px + 'px';
  refreshHitAreas();
});

setupBridge();
updateEmptyHint();
</script>
</body>
</html>
"""


@dataclass
class CanvasItem:
    item_id: str
    tree: Expr
    x: float = 0.0
    y: float = 0.0
    note: str = ""


class SelectionBridge(QObject):
    changed = Signal(str, str)
    swapRequested = Signal(str, str, int)
    expandRequested = Signal(str, str)
    moved = Signal(str, float, float)
    placed = Signal(str, float, float)
    nodeDropped = Signal(str, str, str)
    transformRequested = Signal(str, str)
    copyRequested = Signal(str)
    deleteRequested = Signal(str)
    systemRequested = Signal(str, str)
    collapseToggled = Signal(str, bool)
    cardSelected = Signal(str)
    titleChanged = Signal(str, str)
    nodeCanvasDropped = Signal(str, str, float, float)
    expressionPairRequested = Signal(str, str)

    @Slot(str, str)
    def select(self, item_id: str, node_id: str) -> None:
        self.changed.emit(item_id, node_id)

    @Slot()
    def clear(self) -> None:
        self.changed.emit("", "")

    @Slot(str, str, int)
    def swap(self, item_id: str, node_id: str, index: int) -> None:
        self.swapRequested.emit(item_id, node_id, index)

    @Slot(str, str)
    def expand(self, item_id: str, node_id: str) -> None:
        self.expandRequested.emit(item_id, node_id)

    @Slot(str, float, float)
    def moveItem(self, item_id: str, x: float, y: float) -> None:
        self.moved.emit(item_id, x, y)

    @Slot(str, float, float)
    def placeItem(self, item_id: str, x: float, y: float) -> None:
        self.placed.emit(item_id, x, y)

    @Slot(str, str, str)
    def dropNode(self, source_id: str, node_id: str, target_id: str) -> None:
        self.nodeDropped.emit(source_id, node_id, target_id)

    @Slot(str, str)
    def transform(self, item_id: str, node_id: str) -> None:
        self.transformRequested.emit(item_id, node_id)

    @Slot(str)
    def copyItem(self, item_id: str) -> None:
        self.copyRequested.emit(item_id)

    @Slot(str)
    def deleteItem(self, item_id: str) -> None:
        self.deleteRequested.emit(item_id)

    @Slot(str, str)
    def openSystem(self, first_id: str, second_id: str) -> None:
        self.systemRequested.emit(first_id, second_id)

    @Slot(str, bool)
    def setCollapsed(self, item_id: str, collapsed: bool) -> None:
        self.collapseToggled.emit(item_id, collapsed)

    @Slot(str)
    def selectCard(self, item_id: str) -> None:
        self.cardSelected.emit(item_id)

    @Slot(str, str)
    def setTitle(self, item_id: str, title: str) -> None:
        self.titleChanged.emit(item_id, title)

    @Slot(str, str, float, float)
    def dropNodeOnCanvas(self, item_id: str, node_id: str, x: float, y: float) -> None:
        self.nodeCanvasDropped.emit(item_id, node_id, x, y)

    @Slot(str, str)
    def openExpressionPair(self, dragged_id: str, target_id: str) -> None:
        self.expressionPairRequested.emit(dragged_id, target_id)


DIALOG_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<script>window.MathJax = {
  tex: {displayMath: [['$$', '$$']]},
  svg: {fontCache: 'local'},
  startup: {typeset: false}
};</script>
<script src="../mathjax/es5/tex-svg.js"></script>
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>
<style>
  html, body {margin: 0; height: 100%; background: #ffffff; overflow: hidden;}
  #stage {
    height: 100vh; box-sizing: border-box; padding: 18px;
    display: flex; align-items: center; justify-content: center; overflow: auto;
  }
  #formula {font-size: 34px; color: #1f2328; text-align: center;}
  svg {color: #1f2328;}
  g[id*="__l0-"] {color: #e53935;}
  g[id*="__l1-"] {color: #2e7d32;}
  g[id*="__l2-"] {color: #1565c0;}
  g[id*="__l3-"] {color: #6a1b9a;}
  g[id*="__l"] {cursor: pointer;}
  #formula.error {
    color: #cf222e; font: 14px/1.6 "Microsoft YaHei", sans-serif;
    white-space: pre-wrap; max-width: 520px;
  }
  #selection-box {
    position: fixed; display: none; pointer-events: none; z-index: 20;
    border: 1.5px dashed #0969da; border-radius: 6px; box-sizing: border-box;
  }
  #selection-tag {
    position: fixed; display: none; pointer-events: none; z-index: 21;
    padding: 2px 7px; border-radius: 4px; background: #ffffff;
    border: 1px solid currentColor;
    font: 12px/1.4 "Microsoft YaHei", sans-serif; white-space: nowrap;
  }
</style>
</head>
<body>
<div id="stage"><div id="formula"></div></div>
<div id="selection-box"></div>
<div id="selection-tag"></div>
<script>
const SVG_NS = 'http://www.w3.org/2000/svg';
let nodeMeta = {};
let selectedId = null;
let hoverNode = null;
let hoverRect = null;

function hideSelection() {
  document.getElementById('selection-box').style.display = 'none';
  document.getElementById('selection-tag').style.display = 'none';
}

function clearSelection(notify) {
  selectedId = null;
  hideSelection();
  if (notify && window.bridge && window.bridge.clear) {
    try { window.bridge.clear(); } catch (err) {}
  }
}

function setHover(group) {
  if (group === hoverNode) return;
  if (!group || !group.__hitBox) {
    if (hoverRect) hoverRect.remove();
    hoverNode = null;
    return;
  }
  if (!hoverRect) {
    hoverRect = document.createElementNS(SVG_NS, 'rect');
    hoverRect.setAttribute('fill', '#000000');
    hoverRect.setAttribute('fill-opacity', '0.08');
    hoverRect.setAttribute('pointer-events', 'none');
  }
  const area = group.__hitBox;
  hoverRect.setAttribute('x', area.x);
  hoverRect.setAttribute('y', area.y);
  hoverRect.setAttribute('width', area.width);
  hoverRect.setAttribute('height', area.height);
  hoverRect.setAttribute('rx', 4 * (group.__unitsPerPx || 1));
  const first = group.firstChild;
  const anchor = (first && first.classList && first.classList.contains('hit-area'))
    ? first.nextSibling : first;
  group.insertBefore(hoverRect, anchor);
  hoverNode = group;
}

function installHitAreas() {
  const host = document.getElementById('formula');
  const svg = host.querySelector('svg');
  if (!svg) return;
  host.querySelectorAll('.hit-area').forEach(function (rect) { rect.remove(); });
  const viewBox = svg.viewBox.baseVal;
  const svgRect = svg.getBoundingClientRect();
  const unitsPerPx = (viewBox && svgRect.width) ? viewBox.width / svgRect.width : 1;
  const pad = 5 * unitsPerPx;
  const groups = Array.from(host.querySelectorAll('g[id]')).filter(function (group) {
    return group.id.indexOf('__l') >= 0;
  });
  const boxes = [];
  for (const group of groups) {
    let box = null;
    try { box = group.getBBox(); } catch (err) { box = null; }
    boxes.push([group, box]);
  }
  for (const [group, box] of boxes) {
    if (!box || !isFinite(box.width) || !isFinite(box.height)) continue;
    if (box.width <= 0 || box.height <= 0) continue;
    const area = {
      x: box.x - pad, y: box.y - pad,
      width: box.width + 2 * pad, height: box.height + 2 * pad
    };
    group.__hitBox = area;
    group.__padPx = 5;
    group.__unitsPerPx = unitsPerPx;
    const rect = document.createElementNS(SVG_NS, 'rect');
    rect.setAttribute('class', 'hit-area');
    rect.setAttribute('x', area.x);
    rect.setAttribute('y', area.y);
    rect.setAttribute('width', area.width);
    rect.setAttribute('height', area.height);
    rect.setAttribute('fill', 'transparent');
    rect.setAttribute('pointer-events', 'all');
    group.insertBefore(rect, group.firstChild);
  }
}

function selectNode(group) {
  const id = group.id;
  const meta = nodeMeta[id] || {};
  const padPx = group.__padPx || 0;
  const raw = group.getBoundingClientRect();
  const rect = {
    left: raw.left + padPx, top: raw.top + padPx,
    width: raw.width - 2 * padPx, height: raw.height - 2 * padPx
  };
  rect.right = rect.left + rect.width;
  rect.bottom = rect.top + rect.height;
  const color = getComputedStyle(group).color || '#0969da';
  const box = document.getElementById('selection-box');
  const tag = document.getElementById('selection-tag');
  box.style.display = 'block';
  box.style.left = (rect.left - 5) + 'px';
  box.style.top = (rect.top - 5) + 'px';
  box.style.width = (rect.width + 10) + 'px';
  box.style.height = (rect.height + 10) + 'px';
  box.style.borderColor = color;
  box.style.background = 'transparent';
  tag.style.display = 'block';
  tag.style.color = color;
  tag.textContent = (meta.type || '节点') + ' · 第 ' + (meta.depth === undefined ? '?' : meta.depth) + ' 层';
  const above = rect.top - 28;
  tag.style.left = Math.max(4, rect.left) + 'px';
  tag.style.top = (above > 4 ? above : rect.bottom + 8) + 'px';
  selectedId = id;
  if (window.bridge && window.bridge.select) {
    try { window.bridge.select(id); } catch (err) {}
  }
}

function selectById(id) {
  const group = document.getElementById(id);
  if (group) selectNode(group);
}

document.addEventListener('click', function (event) {
  const target = event.target;
  const group = target && target.closest ? target.closest('g[id*="__l"]') : null;
  if (group) {
    selectNode(group);
  } else {
    clearSelection(true);
  }
});
document.addEventListener('mousemove', function (event) {
  const target = event.target;
  const group = target && target.closest ? target.closest('g[id*="__l"]') : null;
  setHover(group);
});
window.addEventListener('scroll', hideSelection, true);

function setupBridge() {
  if (window.QWebChannel && window.qt && qt.webChannelTransport) {
    new QWebChannel(qt.webChannelTransport, function (channel) {
      window.bridge = channel.objects.bridge;
    });
  }
}

function renderFormula(source, meta) {
  nodeMeta = meta || {};
  const host = document.getElementById('formula');
  clearSelection(false);
  setHover(null);
  host.classList.remove('error');
  host.textContent = '$$' + source + '$$';
  return MathJax.startup.promise
    .then(function () { return MathJax.typesetPromise([host]); })
    .then(function () { installHitAreas(); })
    .catch(function (err) {
      host.classList.add('error');
      host.textContent = String(err);
    });
}

setupBridge();
</script>
</body>
</html>
"""


class DialogBridge(QObject):
    selected = Signal(str)

    @Slot(str)
    def select(self, node_id: str) -> None:
        self.selected.emit(node_id)

    @Slot()
    def clear(self) -> None:
        self.selected.emit("")


class ExpressionDialog(QDialog):
    """在对话框内对表达式做节点级操作。"""

    BASE_OPERATIONS = (
        ("replace", "替换"),
        ("add", "加"),
        ("sub", "减"),
        ("mul", "乘"),
        ("div", "除"),
        ("pow", "乘方"),
    )
    DIV_OPERATIONS = (
        ("div_mul", "上下同乘"),
        ("div_div", "上下同除"),
    )

    def __init__(self, tree: Expr, source: Expr, parent=None) -> None:
        super().__init__(parent)
        self.tree = tree.copy()
        self.source = source.copy()
        self.result_tree = None
        self.node_map: dict = {}
        self.node_info: dict = {}
        self.selected_node = None
        self.operation = None

        self.setWindowTitle("重叠的表达式")
        self.resize(980, 580)
        self.setModal(True)

        main = QVBoxLayout(self)
        main.setContentsMargins(12, 12, 12, 10)
        main.setSpacing(8)

        body = QHBoxLayout()
        body.setSpacing(10)

        self.view = QWebEngineView(self)
        self.view.setContextMenuPolicy(Qt.NoContextMenu)
        body.addWidget(self.view, 1)

        panel = QWidget(self)
        panel.setFixedWidth(270)
        right = QVBoxLayout(panel)
        right.setContentsMargins(6, 0, 0, 0)
        right.setSpacing(7)

        title = QLabel("可用操作")
        title.setObjectName("panelTitle")
        right.addWidget(title)

        self.selection_label = QLabel("在左侧点击选择节点")
        self.selection_label.setObjectName("panelInfo")
        self.selection_label.setWordWrap(True)
        self.selection_label.setTextFormat(Qt.RichText)
        right.addWidget(self.selection_label)

        source_text = str(self.source)
        if len(source_text) > 48:
            source_text = source_text[:45] + "..."
        self.source_label = QLabel("拖拽节点：" + type(self.source).__name__ + "\n" + source_text)
        self.source_label.setObjectName("panelHint")
        self.source_label.setWordWrap(True)
        right.addWidget(self.source_label)

        hint = QLabel("运算顺序：选中节点 运算 拖拽节点")
        hint.setObjectName("panelHint")
        hint.setWordWrap(True)
        right.addWidget(hint)

        self.ops_box = QWidget(panel)
        ops_layout = QVBoxLayout(self.ops_box)
        ops_layout.setContentsMargins(0, 4, 0, 0)
        ops_layout.setSpacing(6)
        self._ops = {}
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        for key, label in self.BASE_OPERATIONS:
            self._add_operation(ops_layout, key, label)
        divider = QLabel("Div 专用")
        divider.setObjectName("panelHint")
        ops_layout.addWidget(divider)
        for key, label in self.DIV_OPERATIONS:
            self._add_operation(ops_layout, key, label)
        self.ops_box.setVisible(False)
        right.addWidget(self.ops_box)
        right.addStretch(1)
        body.addWidget(panel)
        main.addLayout(body, 1)

        box = QDialogButtonBox(self)
        self.confirm_button = box.addButton("确认", QDialogButtonBox.ButtonRole.AcceptRole)
        box.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        self.confirm_button.setEnabled(False)
        box.accepted.connect(self._confirm)
        box.rejected.connect(self.reject)
        main.addWidget(box)

        self.setStyleSheet(
            """
            QLabel#panelTitle {font-size: 14px; font-weight: 600; color: #1f2328;}
            QLabel#panelInfo {color: #1f2328; font-size: 12px;}
            QLabel#panelHint {color: #57606a; font-size: 11px;}
            QPushButton#op {
                border: 1px solid #d0d7de; border-radius: 6px;
                padding: 5px 10px; background: #f6f8fa; text-align: left;
                font-size: 12px;
            }
            QPushButton#op:hover {background: #eaeef2;}
            QPushButton#op:checked {
                background: #ddf4ff; border-color: #0969da; color: #0969da;
            }
            QPushButton#op:disabled {color: #8c959f; background: #ffffff;}
            """
        )

        self._bridge = DialogBridge(self)
        self._bridge.selected.connect(self._on_selected)
        self._channel = QWebChannel(self.view.page())
        self._channel.registerObject("bridge", self._bridge)
        self.view.page().setWebChannel(self._channel)
        self.view.loadFinished.connect(self._on_loaded)
        self.view.setHtml(DIALOG_PAGE, QUrl.fromLocalFile(str(BASE_DIR) + "/"))

    def _add_operation(self, layout, key: str, label: str) -> None:
        button = QPushButton(label)
        button.setObjectName("op")
        button.setCheckable(True)
        button.setEnabled(False)
        button.setCursor(Qt.PointingHandCursor)
        button.clicked.connect(partial(self._choose_operation, key))
        self._group.addButton(button)
        layout.addWidget(button)
        self._ops[key] = button

    @Slot(bool)
    def _on_loaded(self, ok: bool) -> None:
        if not ok:
            return
        printer = LatexPrinter(colorize=True, id_prefix="dlg__")
        colored = printer.doprint(self.tree)
        self.node_map = printer.node_map
        self.node_info = printer.node_info
        script = (
            "renderFormula(" + json.dumps(colored) + ", "
            + json.dumps(printer.node_info, ensure_ascii=False) + ")"
        )
        self.view.page().runJavaScript(script)

    def _on_selected(self, node_id: str) -> None:
        if not node_id:
            self.selected_node = None
            self.selection_label.setText("在左侧点击选择节点")
            self.ops_box.setVisible(False)
            self._set_buttons_enabled(False, False)
            self._reset_operation()
            return
        node = self.node_map.get(node_id)
        if node is None:
            return
        self.selected_node = node
        info = self.node_info.get(node_id, {})
        text = info.get("text", str(node))
        if len(text) > 60:
            text = text[:57] + "..."
        self.selection_label.setText(
            "已选中：<b>" + html_lib.escape(info.get("type", type(node).__name__))
            + "</b> · 第 " + str(info.get("depth", "?")) + " 层<br>"
            + html_lib.escape(text)
        )
        is_div = isinstance(node, Div)
        self.ops_box.setVisible(True)
        self._set_buttons_enabled(True, is_div)
        if self.operation in dict(self.DIV_OPERATIONS) and not is_div:
            self._reset_operation()
        else:
            self.confirm_button.setEnabled(self.operation is not None)

    def _set_buttons_enabled(self, base: bool, div: bool) -> None:
        for key, _ in self.BASE_OPERATIONS:
            self._ops[key].setEnabled(base)
        for key, _ in self.DIV_OPERATIONS:
            self._ops[key].setEnabled(div)

    def _choose_operation(self, key: str) -> None:
        if self.selected_node is None:
            return
        if not self._ops[key].isEnabled():
            return
        self.operation = key
        self.confirm_button.setEnabled(True)

    def _reset_operation(self) -> None:
        self.operation = None
        self._group.setExclusive(False)
        for button in self._ops.values():
            button.setChecked(False)
        self._group.setExclusive(True)
        self.confirm_button.setEnabled(False)

    def _confirm(self) -> None:
        if self.selected_node is None or self.operation is None:
            return
        try:
            self._apply(self.selected_node, self.operation)
        except ZeroDivisionError:
            QMessageBox.warning(self, "无法执行", "拖拽节点为零，不能作为除数或乘数。")
            return
        except Exception as exc:
            QMessageBox.warning(self, "无法执行", str(exc))
            return
        self.result_tree = self.tree
        self.accept()

    def _apply(self, node: Expr, kind: str) -> None:
        if kind in ("div_mul", "div_div") and getattr(self.source, "is_zero", False):
            raise ZeroDivisionError("zero")
        source = self.source.copy()
        if kind == "replace":
            new = source
        elif kind == "add":
            new = Add(node.copy(), source)
        elif kind == "sub":
            new = Add(node.copy(), Mul(Integer(-1), source))
        elif kind == "mul":
            new = Mul(node.copy(), source)
        elif kind == "div":
            new = Div(node.copy(), source)
        elif kind == "pow":
            new = Pow(node.copy(), source)
        elif kind == "div_mul":
            if not isinstance(node, Div):
                return
            new = Div(
                Mul(node.numerator.copy(), source),
                Mul(node.denominator.copy(), self.source.copy()),
            )
        elif kind == "div_div":
            if not isinstance(node, Div):
                return
            new = Div(
                Div(node.numerator.copy(), source),
                Div(node.denominator.copy(), self.source.copy()),
            )
        else:
            return
        parent = node.parent
        if parent is None:
            self.tree = new
            return
        index = next((i for i, child in enumerate(parent.args) if child is node), None)
        if index is None:
            return
        if isinstance(parent, Add) and isinstance(new, Add):
            parent.remove(index)
            for offset, term in enumerate(new.args):
                parent.insert(index + offset, term)
            return
        if isinstance(parent, Mul) and isinstance(new, Mul):
            parent.remove(index)
            for offset, factor in enumerate(new.args):
                parent.insert(index + offset, factor)
            return
        node.replace_with(new)


class TransformDialog(QDialog):
    """选择 SymPy 变形或节点操作方式。"""

    TRANSFORMS = (
        ("simplify", "化简 simplify", "通用化简，尝试多种化简策略"),
        ("expand", "展开 expand", "展开括号、幂与乘积"),
        ("factor", "因式分解 factor", "把多项式分解为因式乘积"),
        ("cancel", "约分 cancel", "约去分子与分母的公因式"),
        ("together", "通分 together", "把和式合并为单个分式"),
        ("apart", "拆分 apart", "部分分式分解"),
        ("trigsimp", "三角化简 trigsimp", "使用三角恒等式化简"),
        ("radsimp", "有理化 radsimp", "化简含根式的分母"),
    )
    OPERATIONS = (
        ("op_replace", "替换", "用输入的表达式替换选中节点"),
        ("op_add", "追加（选中 + 输入）", "在选中节点后追加输入表达式，即相加"),
        ("op_mul", "追乘（选中 × 输入）", "在选中节点后乘上输入表达式"),
        ("op_recip", "倒数（1 / 选中）", "把选中节点取倒数"),
        ("op_div", "除以（选中 ÷ 输入）", "用选中节点除以输入表达式"),
        ("op_square", "平方（选中²）", "把选中节点平方"),
        ("op_sqrt", "算术平方根（√选中）", "对选中节点取算术平方根"),
        ("op_pow", "乘方（选中 ^ 输入）", "以输入表达式为指数"),
        ("op_subs", "换元", "输入换元符号 t 与换元式（如 x+1，即令 t = x+1），把整张卡片中的 x 换成 t 的表达式"),
    )
    NEEDS_INPUT = {"op_replace", "op_add", "op_mul", "op_div", "op_pow", "op_subs"}

    def __init__(self, node: Expr, info: dict, parent=None) -> None:
        super().__init__(parent)
        self.method = None
        self.input_tree = None
        self.replace_tree = None
        self.as_copy = False
        self.setWindowTitle("选择变形方式")
        self.resize(500, 580)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 12)
        layout.setSpacing(8)

        text = info.get("text", str(node))
        if len(text) > 60:
            text = text[:57] + "..."
        info_label = QLabel(
            "选中节点：<b>" + html_lib.escape(info.get("type", type(node).__name__))
            + "</b> · 第 " + str(info.get("depth", "?")) + " 层<br>"
            + html_lib.escape(text)
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        self.list = QListWidget(self)
        self._add_group("SymPy 变形", self.TRANSFORMS)
        self._add_group("节点操作", self.OPERATIONS)
        self.list.currentItemChanged.connect(self._on_current_changed)
        self.list.itemDoubleClicked.connect(lambda *_: self.accept())
        layout.addWidget(self.list, 1)

        input_row = QHBoxLayout()
        input_row.setSpacing(8)
        self.input_label = QLabel("输入表达式")
        self.input_label.setFixedWidth(72)
        self.input_edit = QLineEdit(self)
        self.input_edit.setPlaceholderText("例如：x+1")
        self.input_edit.setEnabled(False)
        input_row.addWidget(self.input_label)
        input_row.addWidget(self.input_edit, 1)
        layout.addLayout(input_row)

        self.replace_row = QWidget(self)
        replace_layout = QHBoxLayout(self.replace_row)
        replace_layout.setContentsMargins(0, 0, 0, 0)
        replace_layout.setSpacing(8)
        replace_label = QLabel("换元式")
        replace_label.setFixedWidth(72)
        self.replace_edit = QLineEdit(self.replace_row)
        self.replace_edit.setPlaceholderText("例如：x+1（令 t = x+1）")
        replace_layout.addWidget(replace_label)
        replace_layout.addWidget(self.replace_edit, 1)
        self.replace_row.setVisible(False)
        layout.addWidget(self.replace_row)

        self.desc_label = QLabel("")
        self.desc_label.setObjectName("transformDesc")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

        result_row = QHBoxLayout()
        result_row.setSpacing(10)
        result_row.addWidget(QLabel("结果"))
        self.replace_radio = QRadioButton("覆盖原表达式")
        self.copy_radio = QRadioButton("保存为副本")
        self.replace_radio.setChecked(True)
        group = QButtonGroup(self)
        group.addButton(self.replace_radio)
        group.addButton(self.copy_radio)
        result_row.addWidget(self.replace_radio)
        result_row.addWidget(self.copy_radio)
        result_row.addStretch(1)
        layout.addLayout(result_row)

        box = QDialogButtonBox(self)
        box.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        box.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

        self.setStyleSheet(
            "QLabel#transformDesc {color: #57606a; font-size: 12px;}"
        )
        self.list.setCurrentRow(1)
        _wire_line_edits(self, parent if parent is not None else self)

    def _add_group(self, title: str, entries) -> None:
        header = QListWidgetItem("— " + title + " —")
        header.setFlags(Qt.NoItemFlags)
        self.list.addItem(header)
        for key, label, description in entries:
            item = QListWidgetItem(label)
            item.setData(Qt.UserRole, key)
            item.setData(Qt.UserRole + 1, description)
            self.list.addItem(item)

    def _on_current_changed(self, current, _previous) -> None:
        if current is None:
            self.desc_label.setText("")
            self.input_edit.setEnabled(False)
            return
        key = current.data(Qt.UserRole)
        self.desc_label.setText(current.data(Qt.UserRole + 1) or "")
        self.input_edit.setEnabled(key in self.NEEDS_INPUT)
        substituting = key == "op_subs"
        self.input_label.setText("换元符号" if substituting else "输入表达式")
        self.input_edit.setPlaceholderText("例如：t" if substituting else "例如：x+1")
        self.replace_row.setVisible(substituting)

    def accept(self) -> None:
        item = self.list.currentItem()
        if item is None:
            return
        key = item.data(Qt.UserRole)
        if not key:
            return
        self.replace_tree = None
        if key in self.NEEDS_INPUT:
            text = self.input_edit.text().strip()
            if not text:
                QMessageBox.warning(self, "缺少表达式", "当前操作需要输入一个表达式。")
                return
            try:
                expression = parse_sympy(text)
                self.input_tree = from_sympy(expression, ordered=False)
            except Exception as exc:
                QMessageBox.warning(self, "表达式无效", str(exc))
                return
            if key == "op_subs":
                replace_text = self.replace_edit.text().strip()
                if not replace_text:
                    QMessageBox.warning(self, "缺少换元式", "请填写换元表达式，例如 x+1。")
                    return
                try:
                    self.replace_tree = from_sympy(parse_sympy(replace_text), ordered=False)
                except Exception as exc:
                    QMessageBox.warning(self, "换元式无效", str(exc))
                    return
        else:
            self.input_tree = None
        self.method = key
        self.as_copy = self.copy_radio.isChecked()
        super().accept()


def _normalize_equation_text(edit) -> None:
    """MathLive 返回 Eq(...) 时改写成 a = b，方便解析。"""
    text = edit.text().strip()
    if not text.startswith("Eq("):
        return
    try:
        expression = sympy.sympify(text)
    except Exception:
        return
    if isinstance(expression, sympy.Eq):
        edit.setText(str(expression.lhs) + " = " + str(expression.rhs))


def _open_formula_editor(edit) -> None:
    try:
        from math_input.math_input import open_formula_dialog
    except Exception as exc:
        QMessageBox.warning(edit.window(), "无法打开公式编辑器", str(exc))
        return
    open_formula_dialog(edit)
    _normalize_equation_text(edit)


def _open_cache_dialog(edit) -> None:
    try:
        from ui.huancun import open_cache
    except Exception as exc:
        QMessageBox.warning(edit.window(), "无法打开缓存区", str(exc))
        return
    open_cache(edit)


def _insert_into_cache(window, edit) -> None:
    text = edit.text().strip()
    if not text:
        return
    cache = getattr(window, "cache", None)
    if cache is None:
        return
    if text in cache:
        cache.remove(text)
    cache.insert(0, text)
    action = getattr(edit, "insert_action", None)
    if action is None:
        return
    original = action.icon()
    action.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogApplyButton))
    QTimer.singleShot(800, lambda a=action, o=original: a.setIcon(o))


def _wire_line_edits(root, window) -> None:
    """与主程序一致：给每个文本框加可视化输入 / 打开缓存区 / 存入缓存区。"""
    for edit in root.findChildren(QLineEdit):
        if getattr(edit, "actions_wired", False):
            continue
        edit.actions_wired = True
        edit.input_action = QAction(QIcon.fromTheme("input-keyboard"), "可视化输入", edit)
        edit.input_action.triggered.connect(
            lambda *_args, target=edit: _open_formula_editor(target)
        )
        edit.addAction(edit.input_action, QLineEdit.TrailingPosition)
        edit.cache_action = QAction(QIcon.fromTheme("document-open"), "打开缓存区", edit)
        edit.cache_action.triggered.connect(
            lambda *_args, target=edit: _open_cache_dialog(target)
        )
        edit.addAction(edit.cache_action, QLineEdit.TrailingPosition)
        edit.insert_action = QAction(QIcon.fromTheme("list-add"), "存入缓存区", edit)
        edit.insert_action.triggered.connect(
            lambda *_args, target=edit: _insert_into_cache(window, target)
        )
        edit.addAction(edit.insert_action, QLineEdit.TrailingPosition)


def _parse_point_text(text: str):
    """把 "(a, b)" 解析成 (x 树, y 树)，不是点则返回 None。"""
    text = text.strip()
    if not (text.startswith("(") and text.endswith(")")):
        return None
    inner = text[1:-1]
    depth = 0
    for index, char in enumerate(inner):
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            left = inner[:index].strip()
            right = inner[index + 1:].strip()
            if not left or not right:
                return None
            try:
                return (
                    from_sympy(parse_sympy(left), ordered=False),
                    from_sympy(parse_sympy(right), ordered=False),
                )
            except Exception:
                return None
    return None


def _format_number(value) -> str:
    if value is sympy.oo:
        return "∞"
    if value is -sympy.oo:
        return "-∞"
    return str(value)


def _format_range(value) -> str:
    if isinstance(value, sympy.Interval):
        left = "(" if value.left_open else "["
        right = ")" if value.right_open else "]"
        return left + _format_number(value.start) + ", " + _format_number(value.end) + right
    if isinstance(value, sympy.Union):
        return " ∪ ".join(_format_range(argument) for argument in value.args)
    if isinstance(value, sympy.FiniteSet):
        if not value.args:
            return "∅"
        return "{" + ", ".join(_format_number(item) for item in value.args) + "}"
    return str(value)


def _finite_solution_roots(solutions):
    """从 solveset 的结果中提取有限个根；无限解集返回 None。"""
    if solutions is sympy.S.EmptySet or solutions == sympy.EmptySet:
        return []
    if getattr(solutions, "is_FiniteSet", False):
        return list(solutions)
    if isinstance(solutions, sympy.Intersection):
        roots = []
        for part in solutions.args:
            if getattr(part, "is_FiniteSet", False):
                roots.extend(list(part))
        return roots
    if isinstance(solutions, sympy.Union):
        roots = []
        for part in solutions.args:
            subset = _finite_solution_roots(part)
            if subset is None:
                return None
            roots.extend(subset)
        return roots
    return None


class SolveDialog(QDialog):
    """选择变量与求解范围，对方程节点求解。"""

    def __init__(self, node: Eq, info: dict, parent=None) -> None:
        super().__init__(parent)
        self.node = node
        self.roots = []
        self.setWindowTitle("求解方程")
        self.resize(520, 340)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        text = info.get("text", str(node))
        if len(text) > 80:
            text = text[:77] + "..."
        info_label = QLabel(
            "方程：<b>" + html_lib.escape(text) + "</b>"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        variables = sorted(node.free_symbols, key=lambda item: item.name)
        variable_row = QHBoxLayout()
        variable_row.addWidget(QLabel("求解变量"))
        self.variable_box = QComboBox(self)
        for variable in variables:
            self.variable_box.addItem(variable.name)
        variable_row.addWidget(self.variable_box, 1)
        layout.addLayout(variable_row)

        domain_row = QHBoxLayout()
        domain_row.addWidget(QLabel("求解范围"))
        self.domain_edit = QLineEdit("Reals", self)
        self.domain_edit.setPlaceholderText("Reals / Complexes / Interval(0, 1)")
        domain_row.addWidget(self.domain_edit, 1)
        layout.addLayout(domain_row)

        hint = QLabel("范围使用 SymPy 集合：Reals（默认）、Complexes、Integers、Interval(a, b) 等")
        hint.setObjectName("solveHint")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        self.preview_label = QLabel("")
        self.preview_label.setObjectName("solveHint")
        self.preview_label.setWordWrap(True)
        layout.addWidget(self.preview_label)

        box = QDialogButtonBox(self)
        self.solve_button = box.addButton("求解", QDialogButtonBox.ButtonRole.AcceptRole)
        box.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

        self.setStyleSheet("QLabel#solveHint {color: #57606a; font-size: 11px;}")
        if not variables:
            self.solve_button.setEnabled(False)
            self.preview_label.setText("方程中没有自由变量，无法求解。")

    def _parse_domain(self, text: str):
        locals_dict = {
            "S": sympy.S,
            "Reals": sympy.S.Reals,
            "Complexes": sympy.S.Complexes,
            "Integers": sympy.S.Integers,
            "Naturals": sympy.S.Naturals,
            "Naturals0": sympy.S.Naturals0,
            "Interval": sympy.Interval,
            "FiniteSet": sympy.FiniteSet,
            "Union": sympy.Union,
            "EmptySet": sympy.S.EmptySet,
        }
        domain = sympy.sympify(text, locals=locals_dict)
        if not isinstance(domain, sympy.Set):
            raise TypeError("求解范围必须是一个 SymPy 集合")
        return domain

    def _solve(self) -> bool:
        name = self.variable_box.currentText()
        if not name:
            QMessageBox.warning(self, "无法求解", "请选择一个求解变量。")
            return False
        try:
            domain = self._parse_domain(self.domain_edit.text().strip() or "Reals")
            equation = self.node.to_sympy()
            solutions = sympy.solveset(equation, sympy.Symbol(name), domain)
        except Exception as exc:
            QMessageBox.warning(self, "求解失败", str(exc))
            return False
        roots = _finite_solution_roots(solutions)
        if roots == []:
            QMessageBox.information(self, "无解", "方程在指定范围内没有解。")
            return False
        if roots is None:
            QMessageBox.information(
                self,
                "解集不是有限集",
                "解集为：\n" + str(solutions) + "\n\n当前只能把有限个根添加为卡片。",
            )
            return False
        seen = set()
        unique = []
        for value in roots:
            key = sympy.srepr(value)
            if key not in seen:
                seen.add(key)
                unique.append(value)
        trees = []
        for value in sorted(unique, key=sympy.default_sort_key):
            try:
                trees.append(from_sympy(value, ordered=True))
            except Exception as exc:
                QMessageBox.warning(self, "根转换失败", str(exc))
                return False
        self.roots = trees
        return True

    def accept(self) -> None:
        if self._solve():
            super().accept()


class SystemDialog(QDialog):
    """两张方程卡片重叠时的联立求解窗口。"""

    VARIABLE_PRIORITY = ("x", "y", "z", "t", "u", "v", "w")

    def __init__(self, equations, parent=None) -> None:
        super().__init__(parent)
        self.equations = equations
        self.result_cards = []
        self._updating_checks = False
        self.setWindowTitle("联立方程")
        self.resize(580, 440)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        for index, equation in enumerate(equations, 1):
            label = QLabel("方程 " + str(index) + "：<b>" + html_lib.escape(str(equation)) + "</b>")
            label.setWordWrap(True)
            layout.addWidget(label)

        mode_row = QHBoxLayout()
        self.direct_radio = QRadioButton("直接求解", self)
        self.vieta_radio = QRadioButton("应用韦达定理", self)
        self.direct_radio.setChecked(True)
        mode_group = QButtonGroup(self)
        mode_group.addButton(self.direct_radio, 0)
        mode_group.addButton(self.vieta_radio, 1)
        mode_row.addWidget(self.direct_radio)
        mode_row.addWidget(self.vieta_radio)
        mode_row.addStretch(1)
        layout.addLayout(mode_row)

        free_names = set()
        for equation in equations:
            free_names.update(symbol.name for symbol in equation.free_symbols)
        self.variable_checks = {}
        variable_row = QHBoxLayout()
        variable_row.addWidget(QLabel("自由变量"))
        for name in sorted(free_names):
            check = QCheckBox(name, self)
            check.setChecked(True)
            self.variable_checks[name] = check
            check.toggled.connect(self._on_variable_toggled)
            variable_row.addWidget(check)
        variable_row.addStretch(1)
        layout.addLayout(variable_row)

        self.output_row = QWidget(self)
        output_layout = QHBoxLayout(self.output_row)
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.setSpacing(12)
        output_layout.addWidget(QLabel("生成"))
        self.sum_check = QCheckBox("x₁ + x₂", self.output_row)
        self.product_check = QCheckBox("x₁·x₂", self.output_row)
        self.abs_check = QCheckBox("|x₁ − x₂|", self.output_row)
        self.delta_check = QCheckBox("判别式 Δ", self.output_row)
        for check in (self.sum_check, self.product_check, self.abs_check, self.delta_check):
            output_layout.addWidget(check)
        self.sum_check.setChecked(True)
        self.product_check.setChecked(True)
        output_layout.addStretch(1)
        layout.addWidget(self.output_row)

        self.hint_label = QLabel("")
        self.hint_label.setObjectName("systemHint")
        self.hint_label.setWordWrap(True)
        layout.addWidget(self.hint_label)

        self.info_label = QLabel("")
        self.info_label.setObjectName("systemHint")
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
        layout.addStretch(1)

        box = QDialogButtonBox(self)
        box.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        box.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

        self.setStyleSheet("QLabel#systemHint {color: #57606a; font-size: 11px;}")
        self.direct_radio.toggled.connect(self._on_mode_changed)
        self.vieta_radio.toggled.connect(self._on_mode_changed)
        self._on_mode_changed()

    def _preferred_vieta_variable(self):
        priority = ["x", "y", "z", "t", "u", "v", "w"]
        scores = {}
        for name in self.variable_checks:
            symbol = sympy.Symbol(name)
            degree = 0
            for equation in self.equations:
                try:
                    expression = self._polynomial(equation)
                    degree = max(degree, int(sympy.degree(expression, symbol) or 0))
                except Exception:
                    continue
            order = priority.index(name) if name in priority else len(priority)
            scores[name] = (-degree, order, name)
        if not scores:
            return None
        return min(scores, key=lambda name: scores[name])

    def _on_variable_toggled(self, checked: bool) -> None:
        if self._updating_checks or not self.vieta_radio.isChecked() or not checked:
            return
        sender = self.sender()
        self._updating_checks = True
        for check in self.variable_checks.values():
            if check is not sender and check.isChecked():
                check.setChecked(False)
        self._updating_checks = False

    def _on_mode_changed(self, *_args) -> None:
        if hasattr(self, "output_row"):
            self.output_row.setVisible(self.vieta_radio.isChecked())
        if self.vieta_radio.isChecked():
            self.hint_label.setText(
                "韦达定理：只勾选一个主变量；x/y/z 等变量优先消元，a/b/c 等符号视为参数保留在系数中。"
                "默认选择二次项最明显的变量，可手动改选；下方可勾选要生成的表达式卡片。"
            )
            preferred = self._preferred_vieta_variable()
            self._updating_checks = True
            for name, check in self.variable_checks.items():
                check.setChecked(name == preferred)
            self._updating_checks = False
        else:
            self.hint_label.setText(
                "直接求解：勾选需要求解的自由变量，每个解的每项会生成一张“变量名 = 根”方程卡片。"
            )

    def _selected_names(self):
        return [name for name, check in self.variable_checks.items() if check.isChecked()]

    def _warn(self, title: str, message: str) -> None:
        QMessageBox.warning(self, title, message)

    def _direct_solve(self) -> bool:
        names = self._selected_names()
        if not names:
            self._warn("无法求解", "请至少勾选一个求解变量。")
            return False
        symbols = [sympy.Symbol(name) for name in names]
        equations = [equation.to_sympy() for equation in self.equations]
        try:
            solutions = sympy.solve(equations, symbols, dict=True)
        except Exception as exc:
            self._warn("求解失败", str(exc))
            return False
        if not solutions:
            QMessageBox.information(self, "无解", "联立方程组没有找到解。")
            return False
        cards = []
        for index, solution in enumerate(solutions, 1):
            if not isinstance(solution, dict):
                continue
            for name in names:
                symbol = sympy.Symbol(name)
                if symbol not in solution:
                    continue
                try:
                    root = from_sympy(solution[symbol], ordered=True)
                except Exception as exc:
                    self._warn("根转换失败", str(exc))
                    return False
                cards.append((Eq(Symbol(name), root), "解 " + str(index)))
        if not cards:
            QMessageBox.information(self, "无结果", "求解结果中没有可生成卡片的变量赋值。")
            return False
        self.result_cards = cards
        return True

    def _polynomial(self, equation: Eq):
        sympy_equation = equation.to_sympy()
        expression = sympy.together(sympy_equation.lhs - sympy_equation.rhs)
        return sympy.expand(sympy.fraction(expression)[0])

    @staticmethod
    def _poly_in(expression, variable):
        try:
            numerator = sympy.fraction(sympy.together(expression))[0]
            return sympy.Poly(sympy.expand(numerator), variable, extension=True)
        except Exception:
            return None

    @staticmethod
    def _factor_candidates(expression, variable):
        candidates = [expression]
        try:
            _coefficient, factors = sympy.factor_list(expression, variable)
            candidates.extend(factor for factor, _power in factors)
        except Exception:
            try:
                _coefficient, factors = sympy.factor_list(expression)
                candidates.extend(factor for factor, _power in factors)
            except Exception:
                pass
        return candidates

    def _quadratic_candidates(self, expressions, variable, other_symbols):
        found = []
        diagnostics = []

        def collect(expression, label):
            for candidate in self._factor_candidates(expression, variable):
                polynomial = self._poly_in(candidate, variable)
                if polynomial is None or polynomial.degree() != 2:
                    continue
                coefficients = polynomial.all_coeffs()
                if len(coefficients) != 3 or sympy.simplify(coefficients[0]) == 0:
                    continue
                found.append(polynomial)
                return True
            diagnostics.append(label + ": " + str(expression))
            return False

        def collect_resultants(symbols):
            for other in symbols:
                for first in range(len(expressions)):
                    for second in range(first + 1, len(expressions)):
                        try:
                            resultant = sympy.simplify(
                                sympy.resultant(expressions[first], expressions[second], other)
                            )
                        except Exception:
                            continue
                        if resultant == 0:
                            continue
                        collect(resultant, "消去 " + str(other))

        eliminable = [
            symbol for symbol in other_symbols
            if symbol.name in self.VARIABLE_PRIORITY
        ]
        parameters = [
            symbol for symbol in other_symbols
            if symbol.name not in self.VARIABLE_PRIORITY
        ]
        collect_resultants(eliminable)
        for index, expression in enumerate(expressions, 1):
            collect(expression, "方程 " + str(index))
        collect_resultants(parameters)
        return found, diagnostics

    def _vieta(self) -> bool:
        names = self._selected_names()
        if len(names) != 1:
            self._warn(
                "无法应用韦达定理",
                "请只勾选一个主变量；其余自由变量会作为参数保留在系数中。",
            )
            return False
        if len(self.equations) < 2:
            self._warn("无法应用韦达定理", "韦达定理需要至少两条方程。")
            return False
        variable_name = names[0]
        variable = sympy.Symbol(variable_name)
        other_symbols = [
            sympy.Symbol(name)
            for name in self.variable_checks
            if name != variable_name
        ]
        try:
            expressions = [self._polynomial(equation) for equation in self.equations]
            polynomials, diagnostics = self._quadratic_candidates(
                expressions, variable, other_symbols
            )
        except Exception as exc:
            self._warn("消元失败", str(exc))
            return False
        if not polynomials:
            detail = "\n".join(diagnostics[:4])
            QMessageBox.information(
                self,
                "不是二次方程",
                "未找到关于 " + variable_name + " 的二次多项式。\n\n"
                + detail
                + "\n\n其余自由变量会作为参数保留；请确认主变量选择是否正确。",
            )
            return False
        polynomial = polynomials[0]
        coefficients = polynomial.all_coeffs()
        if len(coefficients) != 3:
            self._warn("无法应用韦达定理", "消元多项式不是标准二次式。")
            return False
        a, b, c = coefficients
        try:
            sum_value = sympy.simplify(-b / a)
            product_value = sympy.simplify(c / a)
            sum_tree = from_sympy(sum_value, ordered=True)
            product_tree = from_sympy(product_value, ordered=True)
        except Exception as exc:
            self._warn("韦达定理失败", str(exc))
            return False
        try:
            discriminant = sympy.simplify(b ** 2 - 4 * a * c)
        except Exception:
            discriminant = b ** 2 - 4 * a * c
        cards = []
        try:
            if self.sum_check.isChecked():
                cards.append((sum_tree, variable_name + "₁ + " + variable_name + "₂"))
            if self.product_check.isChecked():
                cards.append((product_tree, variable_name + "₁·" + variable_name + "₂"))
            if self.abs_check.isChecked():
                distance = sympy.simplify(sympy.sqrt(discriminant) / sympy.Abs(a))
                cards.append((
                    from_sympy(distance, ordered=True),
                    "|" + variable_name + "₁ − " + variable_name + "₂|",
                ))
            if self.delta_check.isChecked():
                cards.append((from_sympy(discriminant, ordered=True), "Δ"))
        except Exception as exc:
            self._warn("无法生成表达式", str(exc))
            return False
        if not cards:
            self._warn("未勾选生成项", "请至少勾选一个要生成的表达式卡片。")
            return False
        self.result_cards = cards
        return True

    def accept(self) -> None:
        if self.vieta_radio.isChecked():
            success = self._vieta()
        else:
            success = self._direct_solve()
        if success:
            super().accept()


COMMON_EQUATIONS = (
    (
        "圆",
        (
            ("标准方程 (x−a)²+(y−b)²=r²", "(x-({a}))**2+(y-({b}))**2=({r})**2", ("a", "b", "r"), "a、b 为圆心坐标，r 为半径"),
        ),
    ),
    (
        "直线",
        (
            ("一般式 Ax+By+C=0", "({A})*x+({B})*y+({C})=0", ("A", "B", "C"), "A、B 不同时为 0"),
            ("斜截式 y=kx+m", "y=({k})*x+({m})", ("k", "m"), "k 为斜率，m 为纵截距"),
        ),
    ),
    (
        "椭圆",
        (
            ("标准方程 x²/a²+y²/b²=1", "x**2/({a})**2+y**2/({b})**2=1", ("a", "b"), "a 为长半轴，b 为短半轴"),
        ),
    ),
    (
        "双曲线",
        (
            ("横轴 x²/a²−y²/b²=1", "x**2/({a})**2-y**2/({b})**2=1", ("a", "b"), "a 为实半轴，b 为虚半轴"),
            ("纵轴 y²/a²−x²/b²=1", "y**2/({a})**2-x**2/({b})**2=1", ("a", "b"), "a 为实半轴，b 为虚半轴"),
        ),
    ),
    (
        "抛物线",
        (
            ("开口向右 y²=2px", "y**2=2*({p})*x", ("p",), "p 为焦点参数"),
            ("开口向左 y²=−2px", "y**2=-2*({p})*x", ("p",), "p 为焦点参数"),
            ("开口向上 x²=2py", "x**2=2*({p})*y", ("p",), "p 为焦点参数"),
            ("开口向下 x²=−2py", "x**2=-2*({p})*y", ("p",), "p 为焦点参数"),
            ("顶点式 y=a(x−h)²+k", "y=({a})*(x-({h}))**2+({k})", ("a", "h", "k"), "a 为开口系数，顶点为 (h, k)"),
        ),
    ),
)


GENERAL_CONDITIONS = (
    ("通过点", (("x0", "横坐标", "例如 2"), ("y0", "纵坐标", "例如 3")), "曲线经过该点", "通过点 ({x0}, {y0})"),
    ("参数关系", (("relation", "方程", "例如 a=2b"),), "参数之间的关系式", "参数关系 {relation}"),
)

TYPE_CONDITIONS = {
    "直线": (
        ("斜率", (("k", "数值", "例如 2"),), "留空即保留参数 k", "斜率 = {k}"),
        ("截距", (("m", "数值", "例如 -1"),), "在 y 轴上的截距", "截距 = {m}"),
    ),
    "圆": (
        ("圆心所在直线", (("line", "方程", "例如 x=1"),), "圆心 (a, b) 在这条直线上", "圆心在 {line}"),
        ("半径", (("r", "数值", "例如 3"),), "留空即保留参数 r", "半径 = {r}"),
    ),
    "椭圆": (
        ("离心率", (("e", "数值", "例如 1/2"),), "0 < e < 1", "离心率 = {e}"),
        ("长轴长", (("L", "数值", "例如 6"),), "等于 2a", "长轴长 = {L}"),
        ("短轴长", (("S", "数值", "例如 4"),), "等于 2b", "短轴长 = {S}"),
        ("焦距", (("F", "数值", "例如 4"),), "等于 2c，且 c² = a² − b²", "焦距 = {F}"),
    ),
    "双曲线": (
        ("离心率", (("e", "数值", "例如 2"),), "e > 1", "离心率 = {e}"),
        ("实轴长", (("L", "数值", "例如 4"),), "等于 2a", "实轴长 = {L}"),
        ("虚轴长", (("S", "数值", "例如 4"),), "等于 2b", "虚轴长 = {S}"),
        ("焦距", (("F", "数值", "例如 4"),), "等于 2c，且 c² = a² + b²", "焦距 = {F}"),
    ),
    "抛物线": (
        ("准线", (("d", "方程或数值", "例如 x=-2"),), "标准形式下使用", "准线 {d}"),
        ("焦点坐标", (("f", "坐标", "例如 (1, 0)"),), "标准形式下使用", "焦点 {f}"),
    ),
}

STANDARD_PARABOLA_VARIANTS = (0, 1, 2, 3)


def _numeric_value(text: str):
    value = parse_sympy(text.strip())
    if not isinstance(value, sympy.Expr) or value.free_symbols:
        raise ValueError("“" + text.strip() + "”不是有效数值")
    if value.is_real is False:
        raise ValueError("“" + text.strip() + "”不是实数")
    return value


def _coordinate_value(text: str, horizontal: bool):
    cleaned = text.strip().strip("()（）").replace("，", ",")
    parts = [part for part in cleaned.split(",") if part.strip()]
    if not parts:
        raise ValueError("请填写坐标，例如 (1, 0)")
    values = [_numeric_value(part) for part in parts]
    if len(values) == 1:
        return values[0]
    return values[0] if horizontal else values[1]


def _directrix_value(text: str):
    expression = parse_sympy(text.strip())
    if isinstance(expression, sympy.Eq):
        left, right = expression.lhs, expression.rhs
        if left.free_symbols:
            left, right = right, left
        expression = left
    if expression.free_symbols:
        raise ValueError("准线应写成 x=-2 或 y=1 这样的形式")
    return expression


def _normalize_line(expression):
    x, y = sympy.Symbol("x"), sympy.Symbol("y")
    for _round in range(2):
        try:
            polynomial = sympy.Poly(expression, x, y)
        except sympy.PolynomialError:
            return expression
        if polynomial.total_degree() > 1:
            return expression
        coefficients = [item for item in polynomial.coeffs() if item != 0]
        if not coefficients:
            return expression
        factor = coefficients[0]
        for item in coefficients[1:]:
            factor = sympy.gcd(factor, item)
        if factor in (0, 1):
            return expression
        expression = sympy.expand(expression / factor)
    return expression


def _solution_is_real(solution, left, right, protected) -> bool:
    """过滤复参数解与退化解：半轴必须是实数且非零。"""
    for symbol, value in solution.items():
        if value.is_real is False:
            return False
        if symbol.name in protected and value.is_zero is True:
            return False
    for expression in (left, right):
        if expression.has(sympy.I) or expression.has(sympy.zoo) or expression.has(sympy.nan):
            return False
    return True


def _term_degree(term) -> int:
    try:
        return sympy.Poly(term, sympy.Symbol("x"), sympy.Symbol("y")).total_degree()
    except sympy.PolynomialError:
        return 1


def _order_terms(expression):
    """把负项排到后面、高次项排到前面，让解出的方程更接近书写习惯。"""
    if isinstance(expression, sympy.Add):
        terms = [_order_terms(child) for child in expression.args]
        indexed = list(enumerate(terms))
        indexed.sort(key=lambda pair: (
            -_term_degree(pair[1]),
            1 if pair[1].could_extract_minus_sign() else 0,
            0 if sympy.Symbol("x") in pair[1].free_symbols else 1,
            pair[0],
        ))
        return sympy.Add(*[term for _index, term in indexed], evaluate=False)
    if isinstance(expression, sympy.Mul):
        return sympy.Mul(*[_order_terms(child) for child in expression.args], evaluate=False)
    if isinstance(expression, sympy.Pow):
        return sympy.Pow(_order_terms(expression.base), _order_terms(expression.exp), evaluate=False)
    return expression


def _condition_equations(type_name, name, variant, param_names, base_expression, values):
    x, y = sympy.Symbol("x"), sympy.Symbol("y")
    params = {key: sympy.Symbol(key) for key in param_names}
    if name == "通过点":
        point = {x: _numeric_value(values["x0"]), y: _numeric_value(values["y0"])}
        return [base_expression.subs(point)]
    if name == "参数关系":
        expression = parse_sympy(values["relation"].strip())
        if isinstance(expression, sympy.Eq):
            expression = expression.lhs - expression.rhs
        if not isinstance(expression, sympy.Expr):
            raise ValueError("关系式无法解析")
        extra = expression.free_symbols - set(params.values())
        if extra:
            raise ValueError("关系式只能包含参数：" + "、".join(param_names))
        return [expression]
    if name == "斜率":
        value = _numeric_value(values["k"])
        if "k" in params:
            return [params["k"] - value]
        return [-params["A"] - value * params["B"]]
    if name == "截距":
        value = _numeric_value(values["m"])
        if "m" in params:
            return [params["m"] - value]
        return [-params["C"] - value * params["B"]]
    if name == "圆心所在直线":
        line = parse_sympy(values["line"].strip())
        if isinstance(line, sympy.Eq):
            line = line.lhs - line.rhs
        if not isinstance(line, sympy.Expr):
            raise ValueError("直线方程无法解析")
        return [line.subs({x: params["a"], y: params["b"]})]
    if name == "半径":
        value = _numeric_value(values["r"])
        if not value > 0:
            raise ValueError("半径必须是正数")
        return [params["r"] - value]
    if name == "离心率":
        value = _numeric_value(values["e"])
        if type_name == "椭圆":
            if not 0 < value < 1:
                raise ValueError("椭圆的离心率需满足 0 < e < 1")
            return [params["a"] ** 2 * (1 - value ** 2) - params["b"] ** 2]
        if not value > 1:
            raise ValueError("双曲线的离心率需大于 1")
        return [params["a"] ** 2 * (value ** 2 - 1) - params["b"] ** 2]
    if name in ("长轴长", "实轴长"):
        value = _numeric_value(values["L"])
        if not value > 0:
            raise ValueError("轴长必须是正数")
        return [2 * params["a"] - value]
    if name in ("短轴长", "虚轴长"):
        value = _numeric_value(values["S"])
        if not value > 0:
            raise ValueError("轴长必须是正数")
        return [2 * params["b"] - value]
    if name == "焦距":
        value = _numeric_value(values["F"])
        if not value > 0:
            raise ValueError("焦距必须是正数")
        if type_name == "椭圆":
            return [params["a"] ** 2 - params["b"] ** 2 - (value / 2) ** 2]
        return [params["a"] ** 2 + params["b"] ** 2 - (value / 2) ** 2]
    if name == "准线":
        distance = _directrix_value(values["d"])
        sign = -2 if variant in (0, 2) else 2
        return [params["p"] - sign * distance]
    if name == "焦点坐标":
        horizontal = variant in (0, 1)
        value = _coordinate_value(values["f"], horizontal)
        sign = 2 if variant in (0, 2) else -2
        return [params["p"] - sign * value]
    raise ValueError("未知条件：" + name)


def _tidy_expression(expression):
    """把模板解析出的数值项折叠：去掉 0 项、1 系数，并算出数值幂。"""
    if isinstance(expression, sympy.Eq):
        return sympy.Eq(
            _tidy_expression(expression.lhs),
            _tidy_expression(expression.rhs),
            evaluate=False,
        )
    if isinstance(expression, sympy.Add):
        terms = []
        for child in expression.args:
            child = _tidy_expression(child)
            if child.is_number and child == 0:
                continue
            terms.append(child)
        if not terms:
            return sympy.Integer(0)
        if len(terms) == 1:
            return terms[0]
        return sympy.Add(*terms, evaluate=False)
    if isinstance(expression, sympy.Mul):
        coefficient = sympy.Integer(1)
        factors = []
        for child in expression.args:
            child = _tidy_expression(child)
            if child.is_number and child.is_rational:
                coefficient = coefficient * child
                continue
            factors.append(child)
        if coefficient == 0:
            return sympy.Integer(0)
        if coefficient != 1:
            factors.insert(0, coefficient)
        if not factors:
            return sympy.Integer(1)
        if len(factors) == 1:
            return factors[0]
        return sympy.Mul(*factors, evaluate=False)
    if isinstance(expression, sympy.Pow):
        base = _tidy_expression(expression.base)
        exponent = _tidy_expression(expression.exp)
        if base.is_number and exponent.is_number:
            return base ** exponent
        return sympy.Pow(base, exponent, evaluate=False)
    return expression


class CommonEquationDialog(QDialog):
    """按三栏选择添加方式与对象：直接填参数，或用几何条件反推参数。"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("添加常用方程")
        self.resize(820, 520)
        self.setModal(True)

        self.result_trees: list = []
        self._values: dict = {}
        self._edits: dict = {}
        self._conditions: list = []
        self._condition_edits: dict = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 12)
        layout.setSpacing(10)

        columns = QHBoxLayout()
        columns.setSpacing(10)

        method_box = QGroupBox("添加方式", self)
        method_layout = QVBoxLayout(method_box)
        method_layout.setContentsMargins(8, 8, 8, 8)
        self.method_list = QListWidget(method_box)
        self.method_list.addItem(QListWidgetItem("直接输入参数"))
        self.method_list.addItem(QListWidgetItem("通过条件创建"))
        self.method_list.setCurrentRow(0)
        method_layout.addWidget(self.method_list, 1)
        self.method_hint = self._hint_label("直接填写参数数值")
        method_layout.addWidget(self.method_hint)
        method_box.setFixedWidth(150)

        self.type_box = QGroupBox("方程类型", self)
        type_layout = QVBoxLayout(self.type_box)
        type_layout.setContentsMargins(8, 8, 8, 8)
        self.type_list = QListWidget(self.type_box)
        for name, _variants in COMMON_EQUATIONS:
            self.type_list.addItem(QListWidgetItem(name))
        type_layout.addWidget(self.type_list, 1)
        self.type_box.setFixedWidth(150)

        self.param_box = QGroupBox("参数", self)
        param_layout = QVBoxLayout(self.param_box)
        param_layout.setContentsMargins(10, 8, 10, 8)
        param_layout.setSpacing(8)

        form_row = QHBoxLayout()
        form_row.setSpacing(8)
        form_row.addWidget(QLabel("形式"))
        self.variant_combo = QComboBox(self.param_box)
        form_row.addWidget(self.variant_combo, 1)
        param_layout.addLayout(form_row)

        self.stack = QStackedWidget(self.param_box)

        self.param_page = QWidget(self.stack)
        param_page_layout = QVBoxLayout(self.param_page)
        param_page_layout.setContentsMargins(0, 0, 0, 0)
        param_page_layout.setSpacing(8)
        self.param_area = QWidget(self.param_page)
        self.param_form = QFormLayout(self.param_area)
        self.param_form.setContentsMargins(0, 0, 0, 0)
        self.param_form.setSpacing(8)
        self.param_form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        param_page_layout.addWidget(self.param_area)
        self.hint_label = self._hint_label("")
        param_page_layout.addWidget(self.hint_label)
        param_page_layout.addStretch(1)
        self.stack.addWidget(self.param_page)

        self.condition_page = QWidget(self.stack)
        condition_layout = QVBoxLayout(self.condition_page)
        condition_layout.setContentsMargins(0, 0, 0, 0)
        condition_layout.setSpacing(8)

        pick_row = QHBoxLayout()
        pick_row.setSpacing(6)
        pick_row.addWidget(QLabel("条件"))
        self.condition_combo = QComboBox(self.condition_page)
        pick_row.addWidget(self.condition_combo, 1)
        self.add_condition_button = QPushButton("添加", self.condition_page)
        self.add_condition_button.setFixedHeight(24)
        self.add_condition_button.clicked.connect(self._add_condition)
        pick_row.addWidget(self.add_condition_button)
        condition_layout.addLayout(pick_row)

        self.condition_area = QWidget(self.condition_page)
        self.condition_form = QFormLayout(self.condition_area)
        self.condition_form.setContentsMargins(0, 0, 0, 0)
        self.condition_form.setSpacing(6)
        self.condition_form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.condition_area.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        condition_layout.addWidget(self.condition_area)

        self.condition_list = QListWidget(self.condition_page)
        self.condition_list.setMinimumHeight(96)
        condition_layout.addWidget(self.condition_list, 1)

        remove_row = QHBoxLayout()
        remove_row.setSpacing(6)
        self.remove_condition_button = QPushButton("删除选中条件", self.condition_page)
        self.remove_condition_button.setFixedHeight(24)
        self.remove_condition_button.clicked.connect(self._remove_condition)
        remove_row.addWidget(self.remove_condition_button)
        remove_row.addStretch(1)
        condition_layout.addLayout(remove_row)

        self.condition_hint = self._hint_label("添加一个或多个条件，确定后联立求解参数")
        condition_layout.addWidget(self.condition_hint)
        self.stack.addWidget(self.condition_page)

        param_layout.addWidget(self.stack, 1)

        columns.addWidget(method_box)
        columns.addWidget(self.type_box)
        columns.addWidget(self.param_box, 1)
        layout.addLayout(columns, 1)

        box = QDialogButtonBox(self)
        box.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        box.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

        self.method_list.currentRowChanged.connect(self._on_method_changed)
        self.type_list.currentRowChanged.connect(self._on_type_changed)
        self.variant_combo.currentIndexChanged.connect(self._on_variant_changed)
        self.condition_combo.currentIndexChanged.connect(self._on_condition_changed)
        self.type_list.setCurrentRow(0)

    def _hint_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setObjectName("commonHint")
        label.setWordWrap(True)
        label.setStyleSheet("QLabel#commonHint {color: #57606a; font-size: 12px;}")
        return label

    def _cache_owner(self):
        parent = self.parent()
        return parent if parent is not None and hasattr(parent, "cache") else self

    def _method_row(self) -> int:
        return max(self.method_list.currentRow(), 0)

    def _variant_index(self) -> int:
        return max(self.variant_combo.currentIndex(), 0)

    def _current_type(self) -> str:
        return COMMON_EQUATIONS[max(self.type_list.currentRow(), 0)][0]

    def _current_variant(self):
        return COMMON_EQUATIONS[max(self.type_list.currentRow(), 0)][1][self._variant_index()]

    def _on_method_changed(self, row: int) -> None:
        if row < 0:
            return
        if row == 0:
            self.type_box.setTitle("方程类型")
            self.param_box.setTitle("参数")
            self.method_hint.setText("直接填写参数数值")
            self.stack.setCurrentWidget(self.param_page)
            return
        self.type_box.setTitle("创建对象")
        self.param_box.setTitle("条件")
        self.method_hint.setText("用条件反推参数")
        self.stack.setCurrentWidget(self.condition_page)
        self._rebuild_condition_combo()

    def _on_type_changed(self, row: int) -> None:
        if row < 0:
            return
        self._store_values()
        self.variant_combo.blockSignals(True)
        self.variant_combo.clear()
        for label, _template, _names, _hint in COMMON_EQUATIONS[row][1]:
            self.variant_combo.addItem(label)
        self.variant_combo.setCurrentIndex(0)
        self.variant_combo.blockSignals(False)
        self._conditions = []
        self._refresh_condition_list()
        self._rebuild_fields()
        self._rebuild_condition_combo()

    def _on_variant_changed(self, _index: int) -> None:
        self._store_values()
        self._rebuild_fields()
        if self._method_row() == 1:
            self._prune_conditions()
            self._rebuild_condition_combo()

    def _store_values(self) -> None:
        for name, edit in self._edits.items():
            self._values[name] = edit.text()

    def _rebuild_fields(self) -> None:
        while self.param_form.rowCount():
            self.param_form.removeRow(0)
        self._edits = {}
        _label, _template, names, hint = self._current_variant()
        for name in names:
            edit = QLineEdit(self.param_area)
            edit.setPlaceholderText("留空保留 " + name)
            edit.setText(self._values.get(name, ""))
            edit.returnPressed.connect(self.accept)
            self.param_form.addRow(name + " =", edit)
            self._edits[name] = edit
        self.hint_label.setText(hint + "；留空表示保留该参数符号。")
        _wire_line_edits(self.param_area, self._cache_owner())
        if self._edits:
            next(iter(self._edits.values())).setFocus()

    def _available_conditions(self) -> list:
        entries = list(GENERAL_CONDITIONS)
        entries.extend(TYPE_CONDITIONS.get(self._current_type(), ()))
        if self._current_type() == "抛物线" and self._variant_index() not in STANDARD_PARABOLA_VARIANTS:
            entries = [entry for entry in entries if entry[0] not in ("准线", "焦点坐标")]
        return entries

    def _condition_spec(self, name: str):
        for entry in self._available_conditions():
            if entry[0] == name:
                return entry
        return None

    def _rebuild_condition_combo(self) -> None:
        self.condition_combo.blockSignals(True)
        self.condition_combo.clear()
        for entry in self._available_conditions():
            self.condition_combo.addItem(entry[0])
        self.condition_combo.blockSignals(False)
        self._rebuild_condition_fields()

    def _on_condition_changed(self, _index: int) -> None:
        self._rebuild_condition_fields()

    def _rebuild_condition_fields(self) -> None:
        while self.condition_form.rowCount():
            self.condition_form.removeRow(0)
        self._condition_edits = {}
        entry = self._condition_spec(self.condition_combo.currentText())
        if entry is None:
            return
        _name, fields, hint, _template = entry
        for key, label, placeholder in fields:
            edit = QLineEdit(self.condition_area)
            edit.setPlaceholderText(placeholder)
            self.condition_form.addRow(label, edit)
            self._condition_edits[key] = edit
        _wire_line_edits(self.condition_area, self._cache_owner())
        if self._condition_edits:
            next(iter(self._condition_edits.values())).setFocus()
        if not self._conditions:
            self.condition_hint.setText(hint)

    def _condition_preview(self, name: str, values: dict):
        _label, template, names, _hint = self._current_variant()
        base = parse_sympy(template.format(**{key: key for key in names}), evaluate=False)
        return _condition_equations(
            self._current_type(),
            name,
            self._variant_index(),
            names,
            base.lhs - base.rhs,
            values,
        )

    def _add_condition(self) -> None:
        entry = self._condition_spec(self.condition_combo.currentText())
        if entry is None:
            return
        name, fields, hint, _template = entry
        values = {key: edit.text().strip() for key, edit in self._condition_edits.items()}
        if not any(values.values()):
            self.condition_hint.setText("请先填写条件数值")
            return
        if any(not text for text in values.values()):
            self.condition_hint.setText("条件填写不完整，请补全或清空")
            return
        try:
            self._condition_preview(name, values)
        except Exception as exc:
            self.condition_hint.setText("条件不可用：" + str(exc))
            return
        self._conditions.append({"name": name, "values": values})
        for edit in self._condition_edits.values():
            edit.clear()
        self._refresh_condition_list()
        self.condition_hint.setText(hint)

    def _refresh_condition_list(self) -> None:
        self.condition_list.clear()
        for item in self._conditions:
            entry = self._condition_spec(item["name"])
            if entry is None:
                continue
            self.condition_list.addItem(QListWidgetItem(entry[3].format(**item["values"])))

    def _remove_condition(self) -> None:
        row = self.condition_list.currentRow()
        if row < 0 or row >= len(self._conditions):
            return
        self._conditions.pop(row)
        self._refresh_condition_list()

    def _prune_conditions(self) -> None:
        available = {entry[0] for entry in self._available_conditions()}
        self._conditions = [item for item in self._conditions if item["name"] in available]
        self._refresh_condition_list()

    def build_text(self) -> str:
        _label, template, names, _hint = self._current_variant()
        mapping = {}
        for name in names:
            edit = self._edits.get(name)
            text = edit.text().strip() if edit is not None else ""
            mapping[name] = text or name
        return template.format(**mapping)

    def build_tree(self) -> Expr:
        equation = parse_sympy(self.build_text(), evaluate=False)
        if not isinstance(equation, sympy.Eq):
            raise ValueError("生成的不是方程，请检查参数")
        try:
            return from_sympy(_tidy_expression(equation), ordered=False)
        except ZeroDivisionError:
            raise ValueError("参数取值使分母为 0，请检查 a、b 等分母参数") from None

    def build_condition_trees(self) -> list:
        if not self._conditions:
            raise ValueError("请至少添加一个条件")
        _label, template, names, _hint = self._current_variant()
        base_equation = parse_sympy(template.format(**{key: key for key in names}), evaluate=False)
        if not isinstance(base_equation, sympy.Eq):
            raise ValueError("方程形式无法解析")
        equations = []
        for item in self._conditions:
            equations.extend(self._condition_preview(item["name"], item["values"]))
        unknowns = [sympy.Symbol(key) for key in names]
        try:
            solutions = sympy.solve(equations, unknowns, dict=True)
        except Exception as exc:
            raise ValueError("联立求解失败：" + str(exc)) from None
        if not solutions:
            raise ValueError("这些条件互相矛盾，或不足以确定参数")
        is_general_line = self._current_type() == "直线" and self._variant_index() == 0
        protected = {"a", "b", "r", "p"}
        trees = []
        seen = set()
        rejected = 0
        for solution in solutions:
            squares = {}
            for symbol, value in solution.items():
                if symbol.name in ("a", "b", "r"):
                    squares[sympy.Pow(symbol, 2)] = sympy.simplify(value ** 2)
            left = base_equation.lhs.subs(squares).subs(solution)
            right = base_equation.rhs.subs(squares).subs(solution)
            if not _solution_is_real(solution, left, right, protected):
                rejected += 1
                continue
            if is_general_line:
                left = _normalize_line(left)
            left = _order_terms(left)
            right = _order_terms(right)
            key = sympy.srepr(left) + "|" + sympy.srepr(right)
            if key in seen:
                continue
            seen.add(key)
            equation = _tidy_expression(sympy.Eq(left, right, evaluate=False))
            trees.append(from_sympy(equation, ordered=False))
        if not trees:
            if rejected:
                raise ValueError(
                    "这些条件在实数范围内无解：解出的半轴为虚数或为零。\n"
                    "椭圆需要 焦距 < 长轴长 且 0 < e < 1；"
                    "双曲线需要 焦距 > 实轴长 且 e > 1。"
                )
            raise ValueError("条件没有产生新的方程")
        return trees

    def build_trees(self) -> list:
        if self._method_row() == 0:
            return [self.build_tree()]
        return self.build_condition_trees()

    def accept(self) -> None:
        try:
            self.result_trees = self.build_trees()
        except Exception as exc:
            QMessageBox.warning(self, "无法生成方程", str(exc))
            return
        super().accept()


class ExpressionPairDialog(QDialog):
    """两张表达式卡片重叠时，用 M、N 组合出一张新卡片。"""

    def __init__(self, covered: Expr, dragged: Expr, parent=None) -> None:
        super().__init__(parent)
        self.covered = covered
        self.dragged = dragged
        self.result_tree = None
        self.setWindowTitle("组合表达式")
        self.resize(560, 320)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        layout.addWidget(self._pair_label("A（被覆盖）", covered))
        layout.addWidget(self._pair_label("B（拖拽）", dragged))

        hint = QLabel("输入含 A、B 的表达式或方程：A 表示被覆盖的表达式，B 表示拖拽的表达式。例如 A+B、A*B、A=B。")
        hint.setObjectName("pairHint")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        self.input_edit = QLineEdit(self)
        self.input_edit.setPlaceholderText("例如：A+B 或 A*B")
        self.input_edit.textChanged.connect(self._update_preview)
        self.input_edit.returnPressed.connect(self.accept)
        layout.addWidget(self.input_edit)

        self.preview_label = QLabel("")
        self.preview_label.setObjectName("pairHint")
        self.preview_label.setWordWrap(True)
        layout.addWidget(self.preview_label)
        layout.addStretch(1)

        box = QDialogButtonBox(self)
        box.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        box.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

        self.setStyleSheet("QLabel#pairHint {color: #57606a; font-size: 12px;}")
        _wire_line_edits(self, parent if parent is not None else self)
        self.input_edit.setFocus()

    def _pair_label(self, title: str, tree: Expr) -> QLabel:
        text = str(tree)
        if len(text) > 70:
            text = text[:68] + "…"
        label = QLabel(title + "：<b>" + html_lib.escape(text) + "</b>")
        label.setWordWrap(True)
        return label

    def _build_tree(self):
        text = self.input_edit.text().strip()
        if not text:
            raise ValueError("请输入含 A、B 的表达式或方程")
        local = {"A": sympy.Symbol("A"), "B": sympy.Symbol("B")}
        try:
            template = from_sympy(parse_sympy(text, local, evaluate=False), ordered=False)
        except Exception:
            raise ValueError("表达式无法解析：只能使用 A、B 和常数") from None
        names = {symbol.name for symbol in template.free_symbols}
        extra = names - {"A", "B"}
        if extra:
            raise ValueError("只能使用 A、B 和常数，不能出现：" + "、".join(sorted(extra)))
        if not names:
            raise ValueError("请输入含 A、B 的表达式或方程")
        result = template.subs(Symbol("A"), self.covered.copy())
        return result.subs(Symbol("B"), self.dragged.copy())

    def _update_preview(self, _text: str) -> None:
        try:
            result = self._build_tree()
        except Exception as exc:
            self.preview_label.setText(str(exc))
            return
        preview = str(result)
        if len(preview) > 90:
            preview = preview[:88] + "…"
        self.preview_label.setText("预览：" + preview)

    def accept(self) -> None:
        try:
            self.result_tree = self._build_tree()
        except Exception as exc:
            QMessageBox.warning(self, "无法组合", str(exc))
            return
        super().accept()


GEOMETRY_TYPES = (
    (
        "distance",
        "点到直线距离",
        "点 P 到直线的距离",
        (("点 P", "point", "p"), ("直线", "line", "line")),
    ),
    (
        "intersection",
        "两直线交点",
        "两条直线的交点坐标",
        (("直线 1", "line", "line1"), ("直线 2", "line", "line2")),
    ),
    (
        "midpoint",
        "交点线段中点",
        "直线与二次曲线的两个交点为端点的线段中点",
        (("直线", "line", "line"), ("二次曲线", "curve", "curve")),
    ),
    (
        "area3",
        "三角形面积（三点）",
        "三个点围成的三角形面积",
        (("点 P1", "point", "p1"), ("点 P2", "point", "p2"), ("点 P3", "point", "p3")),
    ),
    (
        "area_lc",
        "三角形面积（直线+曲线+点）",
        "直线与曲线的两个交点，再与给定点围成三角形",
        (("直线", "line", "line"), ("二次曲线", "curve", "curve"), ("点 P", "point", "p")),
    ),
)


def _line_expression(text: str):
    expression = parse_sympy(text.strip())
    if isinstance(expression, sympy.Eq):
        expression = expression.lhs - expression.rhs
    if not isinstance(expression, sympy.Expr):
        raise ValueError("直线方程无法解析")
    expression = sympy.expand(expression)
    x, y = sympy.Symbol("x"), sympy.Symbol("y")
    try:
        polynomial = sympy.Poly(expression, x, y)
    except sympy.PolynomialError:
        raise ValueError("直线方程必须是 x、y 的一次式") from None
    if polynomial.total_degree() > 1:
        raise ValueError("直线方程必须是 x、y 的一次式")
    if polynomial.total_degree() == 0:
        raise ValueError("直线方程不能是常数")
    return expression


def _line_coefficients(text: str):
    x, y = sympy.Symbol("x"), sympy.Symbol("y")
    expression = _line_expression(text)
    polynomial = sympy.Poly(expression, x, y)
    return (
        polynomial.coeff_monomial(x),
        polynomial.coeff_monomial(y),
        polynomial.coeff_monomial(1),
    )


def _curve_expression(text: str):
    expression = parse_sympy(text.strip())
    if isinstance(expression, sympy.Eq):
        expression = expression.lhs - expression.rhs
    if not isinstance(expression, sympy.Expr):
        raise ValueError("曲线方程无法解析")
    return sympy.expand(expression)


def _intersections(first, second, x, y):
    try:
        solutions = sympy.solve([first, second], [x, y], dict=True)
    except Exception as exc:
        raise ValueError("求解交点失败：" + str(exc)) from None
    points = []
    seen = set()
    for solution in solutions:
        if x not in solution or y not in solution:
            continue
        key = (sympy.srepr(solution[x]), sympy.srepr(solution[y]))
        if key in seen:
            continue
        seen.add(key)
        points.append((sympy.simplify(solution[x]), sympy.simplify(solution[y])))
    return points


def _point_line_distance(point, line_text: str):
    a, b, c = _line_coefficients(line_text)
    x0, y0 = point
    return sympy.simplify(sympy.Abs(a * x0 + b * y0 + c) / sympy.sqrt(a ** 2 + b ** 2))


def _triangle_area(first, second, third):
    value = (
        first[0] * (second[1] - third[1])
        + second[0] * (third[1] - first[1])
        + third[0] * (first[1] - second[1])
    ) / 2
    return sympy.simplify(sympy.Abs(value))


class GeometryDialog(QDialog):
    """按几何类型选择点/直线/曲线，计算距离、交点、中点或面积。"""

    def __init__(self, points, equations=None, expressions=None, parent=None) -> None:
        super().__init__(parent)
        self.points = list(points)
        self.equations = list(equations or [])
        self.expressions = list(expressions or [])
        self.result_tree = None
        self._widgets = {}
        self.setWindowTitle("添加几何表达式")
        self.resize(600, 380)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 12)
        layout.setSpacing(10)

        type_row = QHBoxLayout()
        type_row.setSpacing(8)
        type_row.addWidget(QLabel("几何量"))
        self.type_combo = QComboBox(self)
        for _key, label, _hint, _fields in GEOMETRY_TYPES:
            self.type_combo.addItem(label)
        type_row.addWidget(self.type_combo, 1)
        layout.addLayout(type_row)

        self.form_area = QWidget(self)
        self.form = QFormLayout(self.form_area)
        self.form.setContentsMargins(0, 0, 0, 0)
        self.form.setSpacing(8)
        self.form.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.form_area.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        layout.addWidget(self.form_area)

        self.hint_label = QLabel("")
        self.hint_label.setObjectName("geometryHint")
        self.hint_label.setWordWrap(True)
        layout.addWidget(self.hint_label)
        layout.addStretch(1)

        box = QDialogButtonBox(self)
        box.addButton("确定", QDialogButtonBox.ButtonRole.AcceptRole)
        box.addButton("取消", QDialogButtonBox.ButtonRole.RejectRole)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        layout.addWidget(box)

        self.setStyleSheet("QLabel#geometryHint {color: #57606a; font-size: 12px;}")
        self.type_combo.currentIndexChanged.connect(self._rebuild_fields)
        self._rebuild_fields()

    def _editable_combo(self, items, placeholder):
        combo = QComboBox(self.form_area)
        combo.setEditable(True)
        for text in items:
            combo.addItem(text)
        combo.setCurrentIndex(0 if items else -1)
        combo.lineEdit().setPlaceholderText(placeholder)
        return combo

    def _point_combo(self):
        return self._editable_combo(self.points, "输入坐标 (a, b)，或从下拉选择已有的点")

    def _line_combo(self):
        return self._editable_combo(self.equations, "输入直线方程，或从下拉选择已有的方程卡片")

    def _curve_combo(self):
        items = list(self.equations)
        items.extend(text for text in self.expressions if text not in items)
        return self._editable_combo(items, "输入曲线方程，或从下拉选择已有的卡片")

    def _rebuild_fields(self, *_args) -> None:
        while self.form.rowCount():
            self.form.removeRow(0)
        self._widgets = {}
        spec = GEOMETRY_TYPES[max(self.type_combo.currentIndex(), 0)]
        for label, kind, name in spec[3]:
            if kind == "point":
                widget = self._point_combo()
            elif kind == "line":
                widget = self._line_combo()
            else:
                widget = self._curve_combo()
            self.form.addRow(label, widget)
            self._widgets[name] = widget
        self.hint_label.setText(spec[2])
        _wire_line_edits(self.form_area, self._cache_owner())
        if self._widgets:
            next(iter(self._widgets.values())).setFocus()

    def _point_value(self, combo):
        text = combo.currentText().strip()
        parsed = _parse_point_text(text)
        if parsed is None:
            raise ValueError("点坐标应写成 (a, b)，当前为：" + (text or "空"))
        return parsed[0].to_sympy(), parsed[1].to_sympy()

    def _cache_owner(self):
        parent = self.parent()
        return parent if parent is not None and hasattr(parent, "cache") else self

    def _compute(self):
        spec = GEOMETRY_TYPES[max(self.type_combo.currentIndex(), 0)]
        key = spec[0]
        widgets = self._widgets
        x, y = sympy.Symbol("x"), sympy.Symbol("y")
        if key == "distance":
            point = self._point_value(widgets["p"])
            value = _point_line_distance(point, widgets["line"].currentText())
            return from_sympy(value, ordered=True)
        if key == "intersection":
            first = _line_expression(widgets["line1"].currentText())
            second = _line_expression(widgets["line2"].currentText())
            points = _intersections(first, second, x, y)
            if not points:
                raise ValueError("两条直线没有交点（可能平行）")
            return Point(from_sympy(points[0][0], ordered=True), from_sympy(points[0][1], ordered=True))
        if key == "midpoint":
            line = _line_expression(widgets["line"].currentText())
            curve = _curve_expression(widgets["curve"].currentText())
            points = _intersections(line, curve, x, y)
            if len(points) != 2:
                raise ValueError("直线与二次曲线应有 2 个交点，实际得到 " + str(len(points)) + " 个")
            middle_x = sympy.simplify((points[0][0] + points[1][0]) / 2)
            middle_y = sympy.simplify((points[0][1] + points[1][1]) / 2)
            return Point(from_sympy(middle_x, ordered=True), from_sympy(middle_y, ordered=True))
        if key == "area3":
            first = self._point_value(widgets["p1"])
            second = self._point_value(widgets["p2"])
            third = self._point_value(widgets["p3"])
            return from_sympy(_triangle_area(first, second, third), ordered=True)
        if key == "area_lc":
            line = _line_expression(widgets["line"].currentText())
            curve = _curve_expression(widgets["curve"].currentText())
            points = _intersections(line, curve, x, y)
            if len(points) != 2:
                raise ValueError("直线与二次曲线应有 2 个交点，实际得到 " + str(len(points)) + " 个")
            third = self._point_value(widgets["p"])
            value = _triangle_area(points[0], points[1], third)
            return from_sympy(value, ordered=True)
        raise ValueError("未知几何量")

    def accept(self) -> None:
        try:
            self.result_tree = self._compute()
        except Exception as exc:
            QMessageBox.warning(self, "无法计算", str(exc))
            return
        super().accept()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("表达式画布 — 分层着色、节点操作与拖拽布局")
        self.resize(1060, 860)
        self._items: list[CanvasItem] = []
        self._item_infos: dict = {}
        self._item_maps: dict = {}
        self._next_item_id = 1
        self._dialog = None
        self._transform_dialog = None
        self._system_dialog = None
        self._equation_dialog = None
        self._pair_dialog = None
        self._geometry_dialog = None
        self._group_item_ids: set = set()
        self._history: list = [[]]
        self._history_index = 0
        self._collapsed: set = set()
        self.cache: list = []
        self.fs: dict = {}
        self._titles: dict = {}
        self._range_cache: dict = {}
        self._build_ui()
        self.view.loadFinished.connect(self._on_page_loaded)

    def _build_ui(self) -> None:
        central = QWidget(self)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(18, 14, 18, 12)
        layout.setSpacing(8)

        hint = QLabel("输入表达式或方程（如 x^2=4），按回车或点击“添加”加入画布")
        hint.setObjectName("hint")

        self.count_label = QLabel("0 个表达式")
        self.count_label.setObjectName("count")

        self.undo_button = QPushButton("撤销")
        self.redo_button = QPushButton("重做")
        for button in (self.undo_button, self.redo_button):
            button.setObjectName("history")
            button.setFixedHeight(26)
            button.setEnabled(False)
            button.setCursor(Qt.PointingHandCursor)
        self.undo_button.clicked.connect(self.undo)
        self.redo_button.clicked.connect(self.redo)

        self.equation_button = QPushButton("添加常用方程")
        self.equation_button.setObjectName("equation")
        self.equation_button.setFixedHeight(26)
        self.equation_button.setCursor(Qt.PointingHandCursor)
        self.equation_button.clicked.connect(self._on_common_equation)

        self.geometry_button = QPushButton("添加几何表达式")
        self.geometry_button.setObjectName("geometry")
        self.geometry_button.setFixedHeight(26)
        self.geometry_button.setCursor(Qt.PointingHandCursor)
        self.geometry_button.clicked.connect(self._on_geometry)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.addWidget(hint)
        top_row.addStretch(1)
        top_row.addWidget(self.count_label)
        top_row.addSpacing(6)
        top_row.addWidget(self.geometry_button)
        top_row.addSpacing(6)
        top_row.addWidget(self.equation_button)
        top_row.addSpacing(6)
        top_row.addWidget(self.undo_button)
        top_row.addWidget(self.redo_button)

        self.input = QLineEdit()
        self.input.setPlaceholderText("例如：2*(x+1) + 1/(x-1) 或 x^2=4")
        self.input.setText("2*(x+1) + 1/(x-1)")
        self.input.returnPressed.connect(self.add_current)

        self.add_button = QPushButton("添加")
        self.add_button.setObjectName("add")
        self.add_button.setFixedHeight(36)
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.add_button.clicked.connect(self.add_current)

        input_row = QHBoxLayout()
        input_row.setContentsMargins(0, 0, 0, 0)
        input_row.setSpacing(8)
        input_row.addWidget(self.input, 1)
        input_row.addWidget(self.add_button)

        self.view = QWebEngineView()
        self.view.setMinimumHeight(360)

        self.properties_panel = self._build_properties_panel()
        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.view)
        self.splitter.addWidget(self.properties_panel)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 0)
        self.splitter.setSizes([760, 220])

        self.detail_view = QPlainTextEdit()
        self.detail_view.setObjectName("detail")
        self.detail_view.setReadOnly(True)
        self.detail_view.setPlaceholderText("点击画布中的节点，查看其自定义结构与 SymPy 表达式")
        self.detail_view.setMinimumHeight(60)
        self.detail_view.setMaximumHeight(92)

        self.selection_label = QLabel("")
        self.selection_label.setObjectName("selection")
        self.selection_label.setTextFormat(Qt.RichText)
        self.selection_label.setWordWrap(True)

        self.status_label = QLabel("")
        self.status_label.setObjectName("status")
        self.status_label.setWordWrap(True)

        layout.addLayout(top_row)
        layout.addLayout(input_row)
        layout.addWidget(self.splitter, 1)
        layout.addWidget(self.detail_view)
        layout.addWidget(self.selection_label)
        layout.addWidget(self.status_label)

        self.setCentralWidget(central)
        self.setStyleSheet(
            """
            QWidget {background: #ffffff; color: #1f2328; font-size: 14px;}
            QLabel#hint {color: #57606a;}
            QLabel#count {color: #57606a; font-size: 12px;}
            QLineEdit {
                border: 1px solid #d0d7de; border-radius: 6px;
                padding: 7px 10px; font-size: 15px;
                selection-background-color: #b6e3ff;
            }
            QLineEdit:focus {border-color: #0969da;}
            QPlainTextEdit#detail {
                border: 1px solid #d0d7de; border-radius: 6px;
                background: #f6f8fa; color: #24292f;
                font-family: Consolas, "Courier New", monospace;
                font-size: 12px; padding: 4px 6px;
            }
            QLabel#selection {color: #57606a; font-size: 13px;}
            QLabel#status {color: #cf222e; font-size: 13px;}
            QPushButton#history {
                border: 1px solid #d0d7de; border-radius: 6px;
                padding: 2px 12px; background: #f6f8fa; color: #24292f;
                font-size: 12px;
            }
            QPushButton#history:hover {background: #eaeef2;}
            QPushButton#history:pressed {background: #dfe3e6;}
            QPushButton#history:disabled {color: #8c959f; background: #ffffff;}
            QPushButton#equation, QPushButton#geometry {
                border: 1px solid #d0d7de; border-radius: 6px;
                padding: 2px 12px; background: #ffffff; color: #0969da;
                font-size: 12px;
            }
            QPushButton#equation:hover, QPushButton#geometry:hover {background: #f6f8fa;}
            QPushButton#equation:pressed, QPushButton#geometry:pressed {background: #eaeef2;}
            QWidget#properties {
                background: #fbfcfd;
                border-left: 1px solid #e5e7eb;
            }
            QWidget#properties QLabel {background: transparent;}
            QLabel#propertiesTitle {color: #1f2328; font-size: 13px;}
            QLabel#propertiesBody {color: #1f2328; font-size: 12px;}
            QSplitter::handle {background: #e5e7eb;}
            QSplitter::handle:horizontal {width: 4px;}
            QPushButton#add {
                border: none; border-radius: 6px; background: #0969da;
                color: #ffffff; font-size: 14px; padding: 0 20px;
            }
            QPushButton#add:hover {background: #0860c4;}
            QPushButton#add:pressed {background: #0757b0;}
            """
        )

        self._bridge = SelectionBridge(self)
        self._bridge.changed.connect(self._on_selection)
        self._bridge.swapRequested.connect(self._on_swap)
        self._bridge.expandRequested.connect(self._on_expand)
        self._bridge.moved.connect(self._on_moved)
        self._bridge.placed.connect(self._on_placed)
        self._bridge.nodeDropped.connect(self._on_node_dropped)
        self._bridge.transformRequested.connect(self._on_transform)
        self._bridge.copyRequested.connect(self._on_copy_item)
        self._bridge.deleteRequested.connect(self._on_delete_item)
        self._bridge.systemRequested.connect(self._on_system_requested)
        self._bridge.collapseToggled.connect(self._on_collapsed)
        self._bridge.cardSelected.connect(self._on_card_selected)
        self._bridge.titleChanged.connect(self._on_title_changed)
        self._bridge.nodeCanvasDropped.connect(self._on_node_canvas_dropped)
        self._bridge.expressionPairRequested.connect(self._on_expression_pair)
        self._channel = QWebChannel(self.view.page())
        self._channel.registerObject("bridge", self._bridge)
        self.view.page().setWebChannel(self._channel)
        self.view.setHtml(PAGE, QUrl.fromLocalFile(str(BASE_DIR) + "/"))

        self._shortcuts = []
        for sequence, slot in (
            (QKeySequence(QKeySequence.StandardKey.Undo), self.undo),
            (QKeySequence(QKeySequence.StandardKey.Redo), self.redo),
            (QKeySequence("Ctrl+Shift+Z"), self.redo),
        ):
            shortcut = QShortcut(sequence, self)
            shortcut.activated.connect(slot)
            self._shortcuts.append(shortcut)

        _wire_line_edits(self, self)
        self.selection_label.setText(
            "拖拽左上角红圈移动表达式 · 点击 + / − 交换相邻项 · 点击括号展开 · 点击节点查看结构"
        )
        if not MATHJAX_FILE.exists():
            self.status_label.setText(f"未找到 MathJax 文件：{MATHJAX_FILE}")

    def _build_properties_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("properties")
        panel.setMinimumWidth(150)
        panel.setMaximumWidth(520)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(14, 12, 14, 12)
        panel_layout.setSpacing(6)
        title = QLabel("属性")
        title.setObjectName("propertiesTitle")
        self.properties_label = QLabel("选中节点或卡片后在此显示属性")
        self.properties_label.setObjectName("propertiesBody")
        self.properties_label.setWordWrap(True)
        self.properties_label.setTextFormat(Qt.RichText)
        self.properties_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        panel_layout.addWidget(title)
        panel_layout.addWidget(self.properties_label)
        panel_layout.addStretch(1)
        return panel

    def _find_item(self, item_id: str):
        return next((item for item in self._items if item.item_id == item_id), None)

    def _item_payload(self, item: CanvasItem):
        printer = LatexPrinter(colorize=True, id_prefix=item.item_id + "__")
        colored = printer.doprint(item.tree)
        return colored, printer.node_info, printer.node_map

    def _store_item(self, item: CanvasItem):
        colored, info, node_map = self._item_payload(item)
        self._item_infos[item.item_id] = info
        self._item_maps[item.item_id] = node_map
        return colored, info, node_map

    def _item_kind(self, item: CanvasItem) -> str:
        if isinstance(item.tree, Eq):
            return "equation"
        if isinstance(item.tree, Point):
            return "point"
        return "expression"

    def _update_count(self) -> None:
        self.count_label.setText(f"{len(self._items)} 个表达式")

    def _clear_detail(self) -> None:
        self.detail_view.clear()

    def _clear_selection(self) -> None:
        self.view.page().runJavaScript("clearSelection(false)")
        self.selection_label.setText(
            "拖拽左上角红圈移动表达式 · 点击 + / − 交换相邻项 · 点击括号展开 · 点击节点查看结构"
        )
        self._clear_detail()
        self._update_properties(None)

    def add_current(self) -> None:
        text = self.input.text().strip()
        if not text:
            return
        coordinates = _parse_point_text(text)
        if coordinates is not None:
            self.status_label.setText("")
            self.input.clear()
            self._add_item(Point(coordinates[0], coordinates[1]))
            self.status_label.setText("已添加点")
            self.input.setFocus()
            return
        try:
            expression = parse_sympy(text)
            tree = from_sympy(expression, ordered=False)
        except Exception as exc:
            self.status_label.setText(f"解析失败：{exc}")
            return
        self.status_label.setText("")
        self.input.clear()
        self._add_item(tree)
        self.input.setFocus()

    def _on_common_equation(self) -> None:
        dialog = CommonEquationDialog(self)
        self._equation_dialog = dialog
        dialog.accepted.connect(lambda: self._add_common_equation(dialog))
        dialog.finished.connect(self._clear_equation_dialog)
        dialog.open()

    def _add_common_equation(self, dialog) -> None:
        trees = getattr(dialog, "result_trees", None) or []
        if not trees:
            return
        self.status_label.setText("")
        if len(trees) == 1:
            self._add_item(trees[0])
            self.status_label.setText("已添加常用方程")
            return
        self._group_item_ids = {self._add_item(tree) for tree in trees}
        self.status_label.setText(f"已添加 {len(trees)} 张方程卡片")

    def _clear_equation_dialog(self, *_args) -> None:
        self._equation_dialog = None

    def _on_collapsed(self, item_id: str, collapsed: bool) -> None:
        if collapsed:
            self._collapsed.add(item_id)
        else:
            self._collapsed.discard(item_id)

    def _on_geometry(self) -> None:
        points = []
        equations = []
        expressions = []
        for item in self._items:
            if isinstance(item.tree, Point):
                text = "(" + str(item.tree.x) + ", " + str(item.tree.y) + ")"
                if text not in points:
                    points.append(text)
                continue
            text = str(item.tree)
            if isinstance(item.tree, Eq):
                if text not in equations:
                    equations.append(text)
            elif text not in expressions:
                expressions.append(text)
        dialog = GeometryDialog(points, equations, expressions, self)
        self._geometry_dialog = dialog
        dialog.accepted.connect(lambda: self._add_geometry_result(dialog))
        dialog.finished.connect(self._clear_geometry_dialog)
        dialog.open()

    def _add_geometry_result(self, dialog) -> None:
        tree = dialog.result_tree
        if tree is None:
            return
        self.status_label.setText("")
        self._add_item(tree)
        self.status_label.setText("已添加点" if isinstance(tree, Point) else "已添加几何表达式")

    def _clear_geometry_dialog(self, *_args) -> None:
        self._geometry_dialog = None

    def _on_node_canvas_dropped(self, item_id: str, node_id: str, x: float, y: float) -> None:
        item = self._find_item(item_id)
        node = self._item_maps.get(item_id, {}).get(node_id)
        if item is None or node is None:
            return
        self._add_item(node.copy(), x=x, y=y)
        self.status_label.setText("已用选中部分生成新卡片")

    def _on_expression_pair(self, dragged_id: str, target_id: str) -> None:
        dragged = self._find_item(dragged_id)
        target = self._find_item(target_id)
        if dragged is None or target is None:
            return
        if not isinstance(dragged.tree, Expr) or not isinstance(target.tree, Expr):
            return
        if isinstance(dragged.tree, (Eq, Point)) or isinstance(target.tree, (Eq, Point)):
            return
        dialog = ExpressionPairDialog(target.tree, dragged.tree, self)
        self._pair_dialog = dialog
        dialog.accepted.connect(lambda: self._apply_expression_pair(dialog))
        dialog.finished.connect(self._clear_pair_dialog)
        dialog.open()

    def _apply_expression_pair(self, dialog) -> None:
        if dialog.result_tree is None:
            return
        self._add_item(dialog.result_tree)
        self.status_label.setText("已用 A、B 组合生成新卡片")

    def _clear_pair_dialog(self, *_args) -> None:
        self._pair_dialog = None

    def _on_card_selected(self, item_id: str) -> None:
        item = self._find_item(item_id)
        if item is None:
            return
        self.view.page().runJavaScript("selectCardById(" + json.dumps(item_id) + ")")
        label = self._titles.get(item_id) or item_id
        self.selection_label.setText("已选中卡片：<b>" + html_lib.escape(label) + "</b>")
        self._clear_detail()
        self._update_properties(item)

    def _on_title_changed(self, item_id: str, title: str) -> None:
        if title:
            self._titles[item_id] = title
        else:
            self._titles.pop(item_id, None)
        if self.selection_label.text().startswith("已选中卡片"):
            item = self._find_item(item_id)
            if item is not None:
                self._update_properties(item)

    def _update_properties(self, item) -> None:
        if item is None:
            self.properties_label.setText(
                "<span style='color:#8c959f'>选中节点或卡片后在此显示属性</span>"
            )
            return
        rows = []
        title = self._titles.get(item.item_id, "")
        if title:
            rows.append("<b>标题</b>　" + html_lib.escape(title))
        if isinstance(item.tree, Point):
            rows.append(
                "<b>坐标</b>　" + html_lib.escape(
                    "(" + str(item.tree.x) + ", " + str(item.tree.y) + ")"
                )
            )
            self.properties_label.setText("<br>".join(rows))
            return
        text = str(item.tree)
        if len(text) > 80:
            text = text[:78] + "…"
        rows.append("<b>表达式</b>　" + html_lib.escape(text))
        symbols = sorted(item.tree.free_symbols, key=lambda symbol: symbol.name)
        if symbols:
            rows.append("<b>变量</b>　" + "、".join(symbol.name for symbol in symbols))
        rows.append("<b>取值范围</b>　" + html_lib.escape(self._range_text(item)))
        self.properties_label.setText("<br>".join(rows))

    def _range_text(self, item: CanvasItem) -> str:
        key = str(item.tree)
        cached = self._range_cache.get(key)
        if cached is None:
            cached = self._compute_range(item.tree)
            self._range_cache[key] = cached
        return cached

    def _compute_range(self, tree: Expr) -> str:
        try:
            expression = tree.to_sympy()
        except Exception:
            return "无法计算"
        if isinstance(expression, sympy.Eq):
            return "方程暂无取值范围"
        symbols = sorted(expression.free_symbols, key=lambda symbol: symbol.name)
        if not symbols:
            return str(expression)
        if len(symbols) > 1:
            return "含多个变量，暂不支持"
        if sympy.count_ops(expression) > 60:
            return "表达式较复杂，暂不计算"
        try:
            from sympy.calculus.util import function_range
            value = function_range(expression, symbols[0], sympy.S.Reals)
        except Exception:
            return "无法计算"
        return _format_range(value)

    def _add_item(
        self,
        tree: Expr,
        note: str = "",
        collapsed: bool = False,
        title: str = "",
        x=None,
        y=None,
    ) -> None:
        item_id = f"c{self._next_item_id}"
        self._next_item_id += 1
        item = CanvasItem(item_id, tree, note=note)
        self._items.append(item)
        if collapsed:
            self._collapsed.add(item_id)
        if title:
            self._titles[item_id] = title
        colored, info, _ = self._store_item(item)
        payload = {
            "id": item_id,
            "latex": colored,
            "plain": str(item.tree),
            "meta": info,
            "kind": self._item_kind(item),
            "note": item.note,
            "title": title,
            "collapsed": item_id in self._collapsed,
        }
        if x is not None and y is not None:
            payload["x"] = float(x)
            payload["y"] = float(y)
        script = "addItem(" + json.dumps(payload, ensure_ascii=False) + ")"
        self.view.page().runJavaScript(script)
        self._update_count()
        return item_id

    def _on_placed(self, item_id: str, x: float, y: float) -> None:
        item = self._find_item(item_id)
        if item is None:
            return
        item.x = float(x)
        item.y = float(y)
        if item_id in self._group_item_ids:
            self._group_item_ids.discard(item_id)
            if not self._group_item_ids:
                self._push_history()
            return
        self._push_history()

    def _on_transform(self, item_id: str, node_id: str) -> None:
        item = self._find_item(item_id)
        node = self._item_maps.get(item_id, {}).get(node_id)
        if item is None or node is None:
            return
        if isinstance(node, Point):
            self.status_label.setText("点是几何对象，暂不支持变形")
            return
        info = self._item_infos.get(item_id, {}).get(node_id, {})
        if isinstance(node, Eq):
            dialog = SolveDialog(node, info, self)
            self._transform_dialog = dialog
            dialog.accepted.connect(lambda: self._add_solution_cards(dialog.roots))
            dialog.finished.connect(self._clear_transform_dialog)
            dialog.open()
            return
        dialog = TransformDialog(node, info, self)
        self._transform_dialog = dialog
        dialog.accepted.connect(
            lambda: self._apply_transform(
                item, node, dialog.method, dialog.input_tree, dialog.as_copy, dialog.replace_tree
            )
        )
        dialog.finished.connect(self._clear_transform_dialog)
        dialog.open()

    def _on_copy_item(self, item_id: str) -> None:
        item = self._find_item(item_id)
        if item is None:
            return
        self._add_item(
            item.tree.copy(),
            note=item.note,
            collapsed=item.item_id in self._collapsed,
            title=self._titles.get(item.item_id, ""),
        )
        self.status_label.setText("已复制卡片")

    def _on_delete_item(self, item_id: str) -> None:
        item = self._find_item(item_id)
        if item is None:
            return
        self._items = [other for other in self._items if other.item_id != item_id]
        self._item_infos.pop(item_id, None)
        self._item_maps.pop(item_id, None)
        self._group_item_ids.discard(item_id)
        self._collapsed.discard(item_id)
        self._titles.pop(item_id, None)
        self.view.page().runJavaScript("removeItem(" + json.dumps(item_id) + ")")
        self._clear_selection()
        self._update_count()
        self._push_history()
        self.status_label.setText("已删除卡片")

    def _on_system_requested(self, first_id: str, second_id: str) -> None:
        first = self._find_item(first_id)
        second = self._find_item(second_id)
        if first is None or second is None:
            return
        if not isinstance(first.tree, Eq) or not isinstance(second.tree, Eq):
            return
        dialog = SystemDialog([first.tree, second.tree], self)
        self._system_dialog = dialog
        dialog.accepted.connect(lambda: self._add_system_cards(dialog.result_cards))
        dialog.finished.connect(self._clear_system_dialog)
        dialog.open()

    def _clear_system_dialog(self, *_args) -> None:
        self._system_dialog = None

    def _add_system_cards(self, cards) -> None:
        if not cards:
            return
        self._group_item_ids = {
            self._add_item(tree, note=note) for tree, note in cards
        }
        self.status_label.setText(f"已添加 {len(cards)} 张联立结果卡片")

    def _add_solution_cards(self, roots) -> None:
        if not roots:
            return
        self._group_item_ids = {self._add_item(root) for root in roots}
        self.status_label.setText(f"已添加 {len(roots)} 个根卡片")

    def _clear_transform_dialog(self, *_args) -> None:
        self._transform_dialog = None

    def _apply_transform(
        self, item: CanvasItem, node: Expr, method, input_tree=None, as_copy=False, replace_tree=None
    ) -> None:
        if not method:
            return
        if method == "op_subs":
            self._apply_substitution(item, input_tree, replace_tree, as_copy)
            return
        try:
            if method.startswith("op_"):
                transformed = self._node_operation(node, method, input_tree)
                if transformed is None:
                    return
            else:
                result = getattr(sympy, method)(node.to_sympy())
                transformed = from_sympy(result, ordered=True)
        except Exception as exc:
            QMessageBox.warning(self, "变形失败", str(exc))
            return
        if as_copy:
            copy_item = CanvasItem(item.item_id, item.tree.copy(), item.x, item.y, item.note)
            path = self._node_path(node)
            copy_node = self._node_at(copy_item.tree, path)
            if self._replace_node(copy_item, copy_node, transformed) is None:
                return
            self._add_item(
                copy_item.tree,
                note=item.note,
                title=self._titles.get(item.item_id, ""),
            )
            self.status_label.setText("已保存为副本")
            return
        target = self._replace_node(item, node, transformed)
        if target is None:
            return
        self.status_label.setText("")
        self._update_item(item, select=target)
        self._push_history()

    def _apply_substitution(self, item: CanvasItem, input_tree, replace_tree, as_copy: bool = False) -> None:
        if not isinstance(input_tree, Symbol):
            QMessageBox.warning(self, "无法换元", "请只输入一个符号，例如 t。")
            return
        if replace_tree is None:
            return
        name = input_tree.name
        card_names = {symbol.name for symbol in item.tree.free_symbols}
        candidates = sorted({symbol.name for symbol in replace_tree.free_symbols} & card_names)
        if not candidates:
            QMessageBox.warning(self, "无法换元", "换元式里的变量没有出现在表达式中。")
            return
        if len(candidates) > 1:
            QMessageBox.warning(self, "无法换元", "换元式只能包含一个变量，例如 x+1。")
            return
        variable_name = candidates[0]
        if name in card_names - {variable_name}:
            QMessageBox.warning(self, "无法换元", f"符号 {name} 已在表达式中使用，请换一个符号。")
            return
        variable = sympy.Symbol(variable_name)
        try:
            solutions = sympy.solve(
                sympy.Eq(sympy.Symbol(name), replace_tree.to_sympy()),
                variable,
                dict=True,
            )
        except Exception as exc:
            QMessageBox.warning(self, "无法换元", "解换元式失败：" + str(exc))
            return
        if not solutions:
            QMessageBox.warning(self, "无法换元", f"无法从换元式解出 {variable_name}，请检查换元式。")
            return
        if len(solutions) > 1:
            QMessageBox.warning(
                self,
                "无法换元",
                f"换元式对 {variable_name} 有多组解（如平方），暂不支持，请改用一次式。",
            )
            return
        replacement = from_sympy(solutions[0][variable], ordered=True)
        base_tree = item.tree.copy() if as_copy else item.tree
        substituted = base_tree.subs(Symbol(variable_name), replacement)
        try:
            substituted = from_sympy(sympy.expand(substituted.to_sympy()), ordered=True)
        except Exception:
            pass
        definition = f"{name} = {replace_tree}"
        if len(definition) > 34:
            definition = definition[:32] + "…"
        note = (item.note + "；" + definition) if item.note else definition
        if as_copy:
            self._add_item(substituted, note=note, title=self._titles.get(item.item_id, ""))
            self.status_label.setText(f"已换元并保存副本：{definition}")
            return
        item.tree = substituted
        item.note = note
        self.status_label.setText(f"已换元：{definition}")
        self._update_item(item)
        self._push_history()

    def _node_operation(self, node: Expr, method: str, input_tree):
        if method == "op_replace":
            return input_tree.copy() if input_tree is not None else None
        if method == "op_add":
            return Add(node.copy(), input_tree.copy())
        if method == "op_mul":
            return Mul(node.copy(), input_tree.copy())
        if method == "op_recip":
            return Div(Integer(1), node.copy())
        if method == "op_div":
            return Div(node.copy(), input_tree.copy())
        if method == "op_square":
            return Pow(node.copy(), Integer(2))
        if method == "op_sqrt":
            return Pow(node.copy(), Rational(1, 2))
        if method == "op_pow":
            return Pow(node.copy(), input_tree.copy())
        return None

    def _node_path(self, node: Expr) -> list:
        path = []
        current = node
        while current.parent is not None:
            path.append(current.index_in_parent)
            current = current.parent
        path.reverse()
        return path

    def _node_at(self, tree: Expr, path) -> Expr:
        current = tree
        for index in path:
            current = current.args[index]
        return current

    def _replace_node(self, item: CanvasItem, node: Expr, new: Expr):
        parent = node.parent
        if parent is None:
            item.tree = new
            return new
        index = next((i for i, child in enumerate(parent.args) if child is node), None)
        if index is None:
            return None
        if isinstance(parent, Add) and isinstance(new, Add):
            parent.remove(index)
            for offset, term in enumerate(new.args):
                parent.insert(index + offset, term)
            item.tree = parent.root
            return parent
        if isinstance(parent, Mul) and isinstance(new, Mul):
            parent.remove(index)
            for offset, factor in enumerate(new.args):
                parent.insert(index + offset, factor)
            item.tree = parent.root
            return parent
        target = node.replace_with(new)
        item.tree = target.root
        return target

    def _on_node_dropped(self, source_id: str, node_id: str, target_id: str) -> None:
        item = self._find_item(target_id)
        source = self._item_maps.get(source_id, {}).get(node_id)
        if item is None or source is None:
            return
        dialog = ExpressionDialog(item.tree, source, self)
        dialog.accepted.connect(partial(self._apply_dialog_result, item, dialog))
        dialog.finished.connect(self._clear_dialog)
        self._dialog = dialog
        dialog.open()

    def _apply_dialog_result(self, item, dialog) -> None:
        if dialog.result_tree is None:
            return
        item.tree = dialog.result_tree
        self._update_item(item)
        self._push_history()
        self._clear_selection()

    def _clear_dialog(self, *_args) -> None:
        self._dialog = None

    def _on_moved(self, item_id: str, x: float, y: float) -> None:
        item = self._find_item(item_id)
        if item is None:
            return
        if abs(item.x - x) < 0.5 and abs(item.y - y) < 0.5:
            return
        item.x = float(x)
        item.y = float(y)
        self._push_history()

    def _on_selection(self, item_id: str, node_id: str) -> None:
        info = self._item_infos.get(item_id, {}).get(node_id) if node_id else None
        node = self._item_maps.get(item_id, {}).get(node_id) if node_id else None
        if info is None or node is None:
            self.selection_label.setText(
                "拖拽左上角红圈移动表达式 · 点击 + / − 交换相邻项 · 点击括号展开 · 点击节点查看结构"
            )
            self._clear_detail()
            self._update_properties(None)
            return
        text = info["text"]
        if len(text) > 80:
            text = text[:77] + "..."
        self.selection_label.setText(
            "已选中：<b>" + html_lib.escape(info["type"]) + "</b> · 第 "
            + str(info["depth"]) + " 层 · <span style='color:"
            + info["color"] + "'>" + html_lib.escape(text) + "</span>"
        )
        self.detail_view.setPlainText(
            "节点结构：" + repr(node) + "\nSymPy：" + str(node.to_sympy())
        )
        self._update_properties(self._find_item(item_id))

    def _id_for(self, node_map: dict, node):
        for node_id, candidate in node_map.items():
            if candidate is node:
                return node_id
        return None

    def _update_item(self, item: CanvasItem, select=None) -> None:
        colored, info, node_map = self._store_item(item)
        select_id = self._id_for(node_map, select) if select is not None else None
        script = (
            "updateItem(" + json.dumps(item.item_id) + ", "
            + json.dumps(colored) + ", "
            + json.dumps(info, ensure_ascii=False) + ", "
            + json.dumps(select_id) + ", "
            + json.dumps(self._item_kind(item)) + ", "
            + json.dumps(item.note, ensure_ascii=False) + ", "
            + json.dumps(str(item.tree)) + ")"
        )
        self.view.page().runJavaScript(script)
        if select_id:
            self._on_selection(item.item_id, select_id)

    def _on_swap(self, item_id: str, node_id: str, index: int) -> None:
        item = self._find_item(item_id)
        node = self._item_maps.get(item_id, {}).get(node_id)
        if item is None or not isinstance(node, Add):
            return
        if index < 0 or index + 1 >= len(node.args):
            return
        node.swap(index, index + 1)
        item.tree = node.root
        self._update_item(item, select=node)
        self._push_history()

    def _on_expand(self, item_id: str, node_id: str) -> None:
        item = self._find_item(item_id)
        node = self._item_maps.get(item_id, {}).get(node_id)
        if item is None or not isinstance(node, Add):
            return
        parent = node.parent
        if isinstance(parent, Mul):
            index = next((i for i, child in enumerate(parent.args) if child is node), None)
            if index is None:
                return
            expanded = parent.expand(index)
        elif isinstance(parent, Pow):
            expanded = parent.expand()
        else:
            return
        self._apply_expansion(item, parent, expanded)

    def _apply_expansion(self, item: CanvasItem, parent, expanded) -> None:
        grand = parent.parent
        if isinstance(grand, Add) and isinstance(expanded, Add):
            position = next((i for i, child in enumerate(grand.args) if child is parent), None)
            if position is None:
                return
            grand.remove(position)
            for offset, term in enumerate(expanded.args):
                grand.insert(position + offset, term)
            item.tree = grand.root
            self._update_item(item, select=grand)
            self._push_history()
            return
        if grand is None:
            item.tree = expanded
            self._update_item(item, select=expanded)
            self._push_history()
            return
        target = parent.replace_with(expanded)
        item.tree = target.root
        self._update_item(item, select=target)
        self._push_history()

    def _snapshot(self):
        return [
            (item.item_id, item.tree.copy(), item.x, item.y, item.note)
            for item in self._items
        ]

    def _push_history(self) -> None:
        self._history = self._history[: self._history_index + 1]
        self._history.append(self._snapshot())
        self._history_index = len(self._history) - 1
        self._update_history_buttons()

    def _update_history_buttons(self) -> None:
        self.undo_button.setEnabled(self._history_index > 0)
        self.redo_button.setEnabled(0 <= self._history_index < len(self._history) - 1)

    def _restore_history(self) -> None:
        self._group_item_ids.clear()
        snapshot = self._history[self._history_index]
        self._items = [
            CanvasItem(item_id, tree.copy(), x, y, note)
            for (item_id, tree, x, y, note) in snapshot
        ]
        self._render_all_items()
        self._clear_selection()
        self._update_count()

    def undo(self) -> None:
        if self._history_index <= 0:
            return
        self._history_index -= 1
        self._restore_history()
        self._update_history_buttons()

    def redo(self) -> None:
        if self._history_index >= len(self._history) - 1:
            return
        self._history_index += 1
        self._restore_history()
        self._update_history_buttons()

    def _render_all_items(self) -> None:
        payload = []
        self._item_infos = {}
        self._item_maps = {}
        for item in self._items:
            colored, info, _ = self._store_item(item)
            payload.append({
                "id": item.item_id,
                "latex": colored,
                "plain": str(item.tree),
                "meta": info,
                "kind": self._item_kind(item),
                "note": item.note,
                "title": self._titles.get(item.item_id, ""),
                "x": item.x,
                "y": item.y,
                "collapsed": item.item_id in self._collapsed,
            })
        script = "setCanvas(" + json.dumps(payload, ensure_ascii=False) + ")"
        self.view.page().runJavaScript(script)

    @Slot(bool)
    def _on_page_loaded(self, ok: bool) -> None:
        if not ok:
            self.status_label.setText("页面加载失败，请检查 ../mathjax/es5/tex-svg.js 是否存在。")
            return
        self._update_count()


def main() -> int:
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    app.setApplicationName("表达式画布")
    app.setFont(QFont("Microsoft YaHei", 10))
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
