"""表达式画布：SymPy → 自定义表达式树 → 分层着色 LaTeX → MathJax。"""

from __future__ import annotations

import html as html_lib
import json
import sys
from dataclasses import dataclass
from functools import partial

import sympy
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QObject, Qt, QUrl, Signal, Slot
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QButtonGroup,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
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
    QVBoxLayout,
    QWidget,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

from expr_calculator.expr_tree import Add, Div, Eq, Expr, Integer, LatexPrinter, Mul, Pow, Rational, Symbol, from_sympy, parse_sympy

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
  if (notify && window.bridge && window.bridge.clear) {
    try { window.bridge.clear(); } catch (err) {}
  }
}

function installHitAreas(item) {
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
  actions.append(copyButton, deleteButton);

  item.append(handle, content, layer, actions);
  if (data.note) {
    const note = document.createElement('div');
    note.className = 'card-note';
    note.textContent = data.note;
    item.appendChild(note);
  }
  return item;
}

function typesetItem(item) {
  const content = item.querySelector('.item-content');
  return MathJax.startup.promise.then(function () {
    return MathJax.typesetPromise([content]);
  });
}

async function addItem(data) {
  const item = createItemElement(data);
  item.style.left = '24px';
  item.style.top = '24px';
  canvas.appendChild(item);
  registerMeta(data.id, data.meta);
  try {
    await typesetItem(item);
    installHitAreas(item);
    installActionAreas(item);
  } catch (err) {
    const content = item.querySelector('.item-content');
    content.classList.add('error');
    content.textContent = String(err);
  }
  const pos = findFreeSpot(item);
  updateEmptyHint();
  try { item.scrollIntoView({block: 'nearest', inline: 'nearest'}); } catch (err) {}
  if (window.bridge && window.bridge.placeItem) {
    try { window.bridge.placeItem(data.id, pos.x, pos.y); } catch (err) {}
  }
}

async function updateItem(itemId, source, meta, selectId, kind, note) {
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
      item.appendChild(noteElement);
    }
    noteElement.textContent = note;
  } else if (noteElement) {
    noteElement.remove();
  }
  const content = item.querySelector('.item-content');
  content.classList.remove('error');
  content.textContent = '$$' + source + '$$';
  try {
    await typesetItem(item);
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
      await typesetItem(item);
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
  } else {
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
    )
    NEEDS_INPUT = {"op_replace", "op_add", "op_mul", "op_div", "op_pow"}

    def __init__(self, node: Expr, info: dict, parent=None) -> None:
        super().__init__(parent)
        self.method = None
        self.input_tree = None
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
        input_label = QLabel("输入表达式")
        self.input_edit = QLineEdit(self)
        self.input_edit.setPlaceholderText("例如：x+1")
        self.input_edit.setEnabled(False)
        input_row.addWidget(input_label)
        input_row.addWidget(self.input_edit, 1)
        layout.addLayout(input_row)

        self.desc_label = QLabel("")
        self.desc_label.setObjectName("transformDesc")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)

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

    def accept(self) -> None:
        item = self.list.currentItem()
        if item is None:
            return
        key = item.data(Qt.UserRole)
        if not key:
            return
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
        else:
            self.input_tree = None
        self.method = key
        super().accept()


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
        if self.vieta_radio.isChecked():
            self.hint_label.setText(
                "韦达定理：只勾选一个主变量；x/y/z 等变量优先消元，a/b/c 等符号视为参数保留在系数中。"
                "默认选择二次项最明显的变量，可手动改选。"
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
        self.result_cards = [
            (sum_tree, variable_name + "₁ + " + variable_name + "₂"),
            (product_tree, variable_name + "₁·" + variable_name + "₂"),
        ]
        return True

    def accept(self) -> None:
        if self.vieta_radio.isChecked():
            success = self._vieta()
        else:
            success = self._direct_solve()
        if success:
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
        self._group_item_ids: set = set()
        self._history: list = [[]]
        self._history_index = 0
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

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.addWidget(hint)
        top_row.addStretch(1)
        top_row.addWidget(self.count_label)
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
        layout.addWidget(self.view, 1)
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

        self.selection_label.setText(
            "拖拽左上角红圈移动表达式 · 点击 + / − 交换相邻项 · 点击括号展开 · 点击节点查看结构"
        )
        if not MATHJAX_FILE.exists():
            self.status_label.setText(f"未找到 MathJax 文件：{MATHJAX_FILE}")

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
        return "equation" if isinstance(item.tree, Eq) else "expression"

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

    def add_current(self) -> None:
        text = self.input.text().strip()
        if not text:
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

    def _add_item(self, tree: Expr, note: str = "") -> None:
        item_id = f"c{self._next_item_id}"
        self._next_item_id += 1
        item = CanvasItem(item_id, tree, note=note)
        self._items.append(item)
        colored, info, _ = self._store_item(item)
        payload = {
            "id": item_id,
            "latex": colored,
            "meta": info,
            "kind": self._item_kind(item),
            "note": item.note,
        }
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
        dialog.accepted.connect(lambda: self._apply_transform(item, node, dialog.method, dialog.input_tree))
        dialog.finished.connect(self._clear_transform_dialog)
        dialog.open()

    def _on_copy_item(self, item_id: str) -> None:
        item = self._find_item(item_id)
        if item is None:
            return
        self._add_item(item.tree.copy(), note=item.note)
        self.status_label.setText("已复制卡片")

    def _on_delete_item(self, item_id: str) -> None:
        item = self._find_item(item_id)
        if item is None:
            return
        self._items = [other for other in self._items if other.item_id != item_id]
        self._item_infos.pop(item_id, None)
        self._item_maps.pop(item_id, None)
        self._group_item_ids.discard(item_id)
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

    def _apply_transform(self, item: CanvasItem, node: Expr, method, input_tree=None) -> None:
        if not method:
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
        target = self._replace_node(item, node, transformed)
        if target is None:
            return
        self.status_label.setText("")
        self._update_item(item, select=target)
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
            + json.dumps(item.note, ensure_ascii=False) + ")"
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
                "meta": info,
                "kind": self._item_kind(item),
                "note": item.note,
                "x": item.x,
                "y": item.y,
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
