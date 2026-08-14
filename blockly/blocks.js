(function() {
  'use strict';

  if (typeof Blockly === 'undefined') return;

  var COLOUR_CALC = 230;
  var COLOUR_EQUATION = 260;
  var COLOUR_IO_INPUT = 160;
  var COLOUR_IO_OUTPUT = 20;

  // ---------------------------------------------------------------------------
  // 自定义积木文案 i18n（zh / en），按 index.html 解析的语言选择
  // ---------------------------------------------------------------------------
  var STRINGS = {
    zh: {
      derivative: '求导', func: '函数', order: '阶数', at: '在x=',
      integral: '积分', lower: '下限', upper: '上限',
      funcAttr: '函数属性', domain: '定义域',
      attrRange: '值域', attrInc: '单调递增', attrDec: '单调递减',
      attrParity: '奇偶性', attrPeriod: '周期', attrMax: '最大值', attrMin: '最小值',
      solveEq: '解方程', equation: '方程',
      exprInput: '表达式',
      defineFunc: '定义函数', name: '名称',
      simplify: '代数式变形',
      mSimplify: '通用化简(simplify)', mExpand: '展开(expand)', mFactor: '因式分解(factor)',
      mCollect: '主元(collect)', mCancel: '通分(cancel)', mApart: '分离(apart)',
      mTrigsimp: '三角变换(trigsimp)', mExpandTrig: '三角展开(expand_trig)',
      mPowsimp: '指数合并(powsimp)', mExpandPow: '指数展开(expand_power_exp)',
      mExpandLog: '对数展开(expand_log)', mLogcombine: '对数合并(logcombine)', mSub: '换元',
      solveEqs: '解方程组', eq1: '方程1(=0)', eq2: '方程2(=0)',
      solveIneq: '解不等式', left: '左式', right: '右式',
      solveIneqSys: '解不等式组',
      solveTri: '解三角形', value: '值', triSelect: '— 选择条件 —',
      angA: '角A', angB: '角B', angC: '角C', sideA: '边a', sideB: '边b', sideC: '边c',
      exprCalc: '代数式计算', callFunc: '调用函数', argVal: '自变量取值(可选)',
      ioInput: '输入 名称', ioOutput: '输出 名称',
      adv: '高级设置', advVar: '变量', advVars: '变量列表',
      advCollect: '主元', advSubBy: '换元符', advSub: '换元式',
      advHint: '高级设置：勾选并连接对应的选项积木，以启用变量、定义域、主元/换元等高级参数。',
      ttDerivative: 'Derivative of a function (order & value optional).',
      ttIntegral: 'Indefinite or definite integral.',
      ttFuncAttr: 'Range / monotonicity / parity / period / extrema of a function.',
      ttSolveEq: 'Solve a one-variable equation.',
      ttExprInput: 'Type a math expression, or connect another block here.',
      ttDefineFunc: 'Define a function into the function dictionary.',
      ttSimplify: 'Simplify, expand or factor an expression.',
      ttSolveEqs: 'Solve a system of equations (each equals 0).',
      ttSolveIneq: 'Solve a one-variable inequality.',
      ttSolveIneqSys: 'Solve a system of two inequalities.',
      ttSolveTri: 'Solve a triangle given three conditions.',
      ttExprCalc: 'Evaluate an expression exactly (SymPy engine).',
      ttCallFunc: 'Call a defined function; pass an argument value or leave empty.',
      ttIoInput: 'Read an input value named NAME from the right panel.',
      ttIoOutput: 'Send a value to the output table (grouped by name).'
    },
    en: {
      derivative: 'Derivative', func: 'Function', order: 'Order', at: 'at x=',
      integral: 'Integral', lower: 'Lower', upper: 'Upper',
      funcAttr: 'Function Properties', domain: 'Domain',
      attrRange: 'Range', attrInc: 'Increasing', attrDec: 'Decreasing',
      attrParity: 'Parity', attrPeriod: 'Period', attrMax: 'Maximum', attrMin: 'Minimum',
      solveEq: 'Solve Equation', equation: 'Equation',
      exprInput: 'Expression',
      defineFunc: 'Define Function', name: 'Name',
      simplify: 'Simplify Expression',
      mSimplify: 'Simplify', mExpand: 'Expand', mFactor: 'Factor',
      mCollect: 'Collect', mCancel: 'Cancel', mApart: 'Apart',
      mTrigsimp: 'Trig simplify', mExpandTrig: 'Expand trig',
      mPowsimp: 'Pow simplify', mExpandPow: 'Expand powers',
      mExpandLog: 'Expand log', mLogcombine: 'Combine log', mSub: 'Substitute',
      solveEqs: 'Solve Equations', eq1: 'Equation 1 (=0)', eq2: 'Equation 2 (=0)',
      solveIneq: 'Solve Inequality', left: 'Left', right: 'Right',
      solveIneqSys: 'Solve Inequality System',
      solveTri: 'Solve Triangle', value: 'Value', triSelect: '— select condition —',
      angA: 'Angle A', angB: 'Angle B', angC: 'Angle C', sideA: 'Side a', sideB: 'Side b', sideC: 'Side c',
      exprCalc: 'Evaluate Expression', callFunc: 'Call Function', argVal: 'Argument value (optional)',
      ioInput: 'Input name', ioOutput: 'Output name',
      adv: 'Advanced settings', advVar: 'Variable', advVars: 'Variables',
      advCollect: 'Collect', advSubBy: 'Substitute by', advSub: 'Substitute expr',
      advHint: 'Advanced settings: enable and connect the option blocks below to show extra parameters such as variable, domain, collect/substitute, etc.',
      ttDerivative: '计算函数的导数，可指定阶数与代入求值。',
      ttIntegral: '计算不定积分或定积分（上下限为空时为不定积分）。',
      ttFuncAttr: '查询函数的值域、单调性、奇偶性、周期或最值。',
      ttSolveEq: '求解一元方程的解集。',
      ttExprInput: '输入数学表达式，或在此连接其他积木。',
      ttDefineFunc: '定义函数并存入函数字典。',
      ttSimplify: '对表达式进行化简、展开、因式分解等变形。',
      ttSolveEqs: '求解方程组（每个方程以 =0 形式输入）。',
      ttSolveIneq: '求解一元不等式的解集。',
      ttSolveIneqSys: '求解由两个不等式组成的不等式组。',
      ttSolveTri: '已知三角形三个条件求解其余元素。',
      ttExprCalc: '使用 SymPy 符号引擎计算表达式的精确值。',
      ttCallFunc: '调用已定义函数；可传自变量取值或留空。',
      ttIoInput: '从右侧输入面板读取名为 NAME 的输入值。',
      ttIoOutput: '将值输出到右侧输出面板（按名称分组）。'
    }
  };
  var S = (window._blocklyLang === 'en') ? STRINGS.en : STRINGS.zh;

  // ---------------------------------------------------------------------------
  // 通用积木定义辅助
  // ---------------------------------------------------------------------------

  // 为指定输入挂载一个 expr_input 表达式影子积木（默认值由 defaultText 决定）。
  function attachTextShadowInput(block, inputName, defaultText) {
    var input = block.appendValueInput(inputName).setCheck('String');
    var shadowBlock = block.workspace.newBlock('expr_input');
    shadowBlock.setFieldValue(defaultText, 'TEXT');
    shadowBlock.setShadow(true);
    input.connection.connect(shadowBlock.outputConnection);
    return input;
  }

  // 注册一个积木定义（type、init 回调）。
  function registerBlock(type, init) {
    Blockly.Blocks[type] = { init: init };
  }

  // 常用"表达式"输入的快捷方式：标签 + shadow 表达式输入框。
  function shadowField(block, inputName, label, defaultText) {
    return attachTextShadowInput(block, inputName, defaultText).appendField(label);
  }

  // ---------------------------------------------------------------------------
  // 高级设置：通过积木左侧的"设置"齿轮按钮（Blockly mutator）展开/收起高级参数。
  // 点击齿轮会弹出一个小工作区，其中列出各高级选项积木；把选项积木连接起来即启用
  // 对应的输入，移走即隐藏。高级参数采用与主参数一致的"可连接积木块输入"
  // （value 输入 + 表达式影子积木），而非内联文本框。
  // advDefs 形如 [{ name, optionType, attr, label, default }]，每个元素对应一个
  // 高级输入。输入默认隐藏；值在隐藏/显示间得以保留（Input.setVisible 仅切换可见性）。
  // ---------------------------------------------------------------------------

  // 高级选项积木（出现在齿轮弹窗中，可堆叠连接）。
  function registerAdvOption(type, label) {
    registerBlock(type, function() {
      this.appendDummyInput().appendField(label);
      this.setPreviousStatement(true);
      this.setNextStatement(true);
      this.setColour(COLOUR_CALC);
      this.setInputsInline(true);
    });
  }
  registerAdvOption('adv_opt_var', S.advVar);
  registerAdvOption('adv_opt_vars', S.advVars);
  registerAdvOption('adv_opt_domain', S.domain);
  registerAdvOption('adv_opt_collect', S.advCollect);
  registerAdvOption('adv_opt_subby', S.advSubBy);
  registerAdvOption('adv_opt_sub', S.advSub);
  registerAdvOption('adv_opt_arg', S.argVal);
  registerAdvOption('adv_opt_order', S.order);
  registerAdvOption('adv_opt_at', S.at);

  // 齿轮弹窗工作区的容器积木（选项积木堆叠其下方）。
  registerBlock('adv_opt_container', function() {
    this.appendDummyInput().appendField(S.adv);
    this.setNextStatement(true);
    this.setColour(COLOUR_CALC);
    this.setInputsInline(true);
  });

  // 高级设置 mutator：将可见的高级输入状态与弹窗中的选项积木同步。
  var ADVANCED_MUTATOR_MIXIN = {
    mutationToDom: function() {
      var container = Blockly.utils.xml.createElement('mutation');
      var self = this;
      (self._advDefs || []).forEach(function(def) {
        if (def.input && def.input.isVisible()) {
          container.setAttribute(def.attr, '1');
        }
      });
      return container;
    },
    domToMutation: function(xml) {
      var self = this;
      (self._advDefs || []).forEach(function(def) {
        if (def.input) def.input.setVisible(xml.getAttribute(def.attr) === '1');
      });
      if (this.rendered) this.render();
    },
    saveExtraState: function() {
      var state = {};
      var hasAny = false;
      var self = this;
      (self._advDefs || []).forEach(function(def) {
        if (def.input && def.input.isVisible()) { state[def.attr] = true; hasAny = true; }
      });
      return hasAny ? state : null;
    },
    loadExtraState: function(state) {
      state = state || {};
      var self = this;
      (self._advDefs || []).forEach(function(def) {
        if (def.input) def.input.setVisible(!!state[def.attr]);
      });
      if (this.rendered) this.render();
    },
    decompose: function(workspace) {
      var container = workspace.newBlock('adv_opt_container');
      container.initSvg();
      var tailConnection = container.nextConnection;
      var self = this;
      (self._advDefs || []).forEach(function(def) {
        if (def.input && def.input.isVisible()) {
          var block = workspace.newBlock(def.optionType);
          block.initSvg();
          tailConnection.connect(block.previousConnection);
          tailConnection = block.nextConnection;
        }
      });
      return container;
    },
    compose: function(containerBlock) {
      var enabled = {};
      var child = containerBlock && containerBlock.nextConnection &&
          containerBlock.nextConnection.targetBlock();
      while (child) {
        if (!child.isInsertionMarker()) enabled[child.type] = true;
        child = child.getNextBlock();
      }
      var self = this;
      (self._advDefs || []).forEach(function(def) {
        if (def.input) def.input.setVisible(!!enabled[def.optionType]);
      });
      if (this.rendered) this.render();
    }
  };

  // 注册"高级设置"mutator（齿轮图标）。第 4 个参数是弹窗中可拖拽的选项积木类型。
  Blockly.Extensions.registerMutator(
    'advanced_settings', ADVANCED_MUTATOR_MIXIN, null,
    ['adv_opt_var', 'adv_opt_vars', 'adv_opt_domain', 'adv_opt_collect',
     'adv_opt_subby', 'adv_opt_sub', 'adv_opt_arg', 'adv_opt_order', 'adv_opt_at']);

  // 为积木挂载高级设置：创建可连接的高级 value 输入（默认隐藏），并应用齿轮 mutator。
  // 每个积木只显示与其功能相关的高级选项（由 advDefs 中的 optionType 决定），
  // 而非所有积木共用同一套选项。
  function addAdvancedSettings(block, advDefs) {
    block._advDefs = advDefs;
    advDefs.forEach(function(def) {
      // value 输入 + 表达式影子积木（与主参数一致），标签在输入之后。
      var input = attachTextShadowInput(block, def.name, def.default);
      input.appendField(def.label);
      input.setVisible(false);
      def.input = input;
    });
    // 应用 mutator 扩展，为积木添加左侧齿轮图标。
    Blockly.Extensions.apply('advanced_settings', block, true);
    // 将齿轮弹窗的飞入区限定为本积木相关的高级选项（避免共用全部选项）。
    if (block.mutator && block.mutator.flyoutBlockTypes) {
      block.mutator.flyoutBlockTypes = advDefs.map(function(def) { return def.optionType; });
    }
  }

  // ---------------------------------------------------------------------------
  // 自定义积木定义（已精简冗余字段，使用内联文本框使积木更紧凑）
  // ---------------------------------------------------------------------------

  // 求导：默认对变量 x 求导；可指定阶数与代入求值。
  registerBlock('calc_derivative', function() {
    this.appendDummyInput().appendField(S.derivative);
    shadowField(this, 'FUNC', S.func, 'x**2');
    addAdvancedSettings(this, [
      { name: 'VAR', optionType: 'adv_opt_var', attr: 'var', label: S.advVar, default: 'x' },
      { name: 'ORDER', optionType: 'adv_opt_order', attr: 'order', label: S.order, default: '1' },
      { name: 'AT', optionType: 'adv_opt_at', attr: 'at', label: S.at, default: '' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_CALC);
    this.setTooltip(S.ttDerivative);
    this.setHelpUrl('');
  });

  // 积分：默认定积分（上下限留空时为不定积分）。
  registerBlock('calc_integral', function() {
    this.appendDummyInput().appendField(S.integral);
    shadowField(this, 'FUNC', S.func, 'x**2');
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput(''), 'LOWER')
        .appendField(S.lower)
        .appendField(new Blockly.FieldTextInput(''), 'UPPER')
        .appendField(S.upper);
    addAdvancedSettings(this, [
      { name: 'VAR', optionType: 'adv_opt_var', attr: 'var', label: S.advVar, default: 'x' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_CALC);
    this.setTooltip(S.ttIntegral);
    this.setHelpUrl('');
  });

  // 函数属性：值域/单调/奇偶/周期/最值。
  registerBlock('calc_function_attr', function() {
    this.appendDummyInput()
        .appendField(S.funcAttr)
        .appendField(new Blockly.FieldDropdown([
          [S.attrRange, '1'],
          [S.attrInc, '2'],
          [S.attrDec, '3'],
          [S.attrParity, '4'],
          [S.attrPeriod, '5'],
          [S.attrMax, '6'],
          [S.attrMin, '7']
        ]), 'ATTR');
    shadowField(this, 'FUNC', S.func, 'x**2');
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput('(-oo, oo)'), 'DOMAIN')
        .appendField(S.domain);
    addAdvancedSettings(this, [
      { name: 'VAR', optionType: 'adv_opt_var', attr: 'var', label: S.advVar, default: 'x' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_CALC);
    this.setTooltip(S.ttFuncAttr);
    this.setHelpUrl('');
  });

  // 解方程：一元方程，默认变量 x。
  registerBlock('solve_equation', function() {
    this.appendDummyInput().appendField(S.solveEq);
    shadowField(this, 'EQ', S.equation, 'x**2-4');
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput('Reals'), 'DOMAIN')
        .appendField(S.domain);
    addAdvancedSettings(this, [
      { name: 'VAR', optionType: 'adv_opt_var', attr: 'var', label: S.advVar, default: 'x' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_EQUATION);
    this.setTooltip(S.ttSolveEq);
    this.setHelpUrl('');
  });

  // 输入：读取右侧输入面板中名为 NAME 的值。
  registerBlock('io_input', function() {
    this.appendDummyInput()
        .appendField(S.ioInput)
        .appendField(new Blockly.FieldTextInput('name'), 'NAME');
    this.setOutput(true, 'String');
    this.setColour(COLOUR_IO_INPUT);
    this.setTooltip(S.ttIoInput);
    this.setHelpUrl('');
  });

  // 输出：将值输出到右侧面板。
  registerBlock('io_output', function() {
    this.appendValueInput('VALUE')
        .setCheck(null)
        .appendField(S.ioOutput)
        .appendField(new Blockly.FieldTextInput('out'), 'NAME');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(COLOUR_IO_OUTPUT);
    this.setTooltip(S.ttIoOutput);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 表达式输入积木：直接编辑文本，输出字符串供其他积木作为值输入连接使用。
  // ---------------------------------------------------------------------------
  registerBlock('expr_input', function() {
    this.appendDummyInput()
        .appendField(S.exprInput)
        .appendField(new Blockly.FieldTextInput('x**2'), 'TEXT');
    this.setOutput(true, 'String');
    this.setColour(COLOUR_CALC);
    this.setTooltip(S.ttExprInput);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 定义函数积木：写入 fs 函数字典，供后续积木引用。
  // ---------------------------------------------------------------------------
  registerBlock('define_func', function() {
    this.appendDummyInput().appendField(S.defineFunc);
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput('f'), 'NAME')
        .appendField(S.name);
    shadowField(this, 'FUNC', S.exprInput, 'x**2');
    addAdvancedSettings(this, [
      { name: 'VAR', optionType: 'adv_opt_var', attr: 'var', label: S.advVar, default: 'x' },
      { name: 'DOMAIN', optionType: 'adv_opt_domain', attr: 'domain', label: S.domain, default: 'Reals' }
    ]);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(COLOUR_CALC);
    this.setTooltip(S.ttDefineFunc);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 代数式变形积木。
  // ---------------------------------------------------------------------------
  var SIMPLIFY_METHODS = [
    [S.mSimplify, '0'],
    [S.mExpand, '1'],
    [S.mFactor, '2'],
    [S.mCollect, '3'],
    [S.mCancel, '4'],
    [S.mApart, '5'],
    [S.mTrigsimp, '6'],
    [S.mExpandTrig, '7'],
    [S.mPowsimp, '8'],
    [S.mExpandPow, '9'],
    [S.mExpandLog, '10'],
    [S.mLogcombine, '11'],
    [S.mSub, '12']
  ];

  registerBlock('expr_simplify', function() {
    this.appendDummyInput()
        .appendField(S.simplify)
        .appendField(new Blockly.FieldDropdown(SIMPLIFY_METHODS), 'METHOD');
    shadowField(this, 'FUNC', S.exprInput, 'x**2+2*x+1');
    addAdvancedSettings(this, [
      { name: 'COLLECT', optionType: 'adv_opt_collect', attr: 'collect', label: S.advCollect, default: 'x' },
      { name: 'SUBBY', optionType: 'adv_opt_subby', attr: 'subby', label: S.advSubBy, default: 't' },
      { name: 'SUB', optionType: 'adv_opt_sub', attr: 'sub', label: S.advSub, default: '' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_CALC);
    this.setTooltip(S.ttSimplify);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 解方程组积木。
  // ---------------------------------------------------------------------------
  registerBlock('solve_equations', function() {
    this.appendDummyInput().appendField(S.solveEqs);
    shadowField(this, 'EQ1', S.eq1, 'x**2-y');
    shadowField(this, 'EQ2', S.eq2, 'x+y-2');
    addAdvancedSettings(this, [
      { name: 'VARS', optionType: 'adv_opt_vars', attr: 'vars', label: S.advVars, default: 'x,y' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_EQUATION);
    this.setTooltip(S.ttSolveEqs);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 解不等式积木。
  // ---------------------------------------------------------------------------
  var INEQUALITY_OPS = [
    ['!=', '!='],
    ['>', '>'],
    ['>=', '>='],
    ['<', '<'],
    ['<=', '<=']
  ];

  registerBlock('solve_inequality', function() {
    this.appendDummyInput()
        .appendField(S.solveIneq)
        .appendField(new Blockly.FieldTextInput('x**2'), 'LHS')
        .appendField(new Blockly.FieldDropdown(INEQUALITY_OPS), 'OP')
        .appendField(new Blockly.FieldTextInput('4'), 'RHS');
    addAdvancedSettings(this, [
      { name: 'VAR', optionType: 'adv_opt_var', attr: 'var', label: S.advVar, default: 'x' },
      { name: 'DOMAIN', optionType: 'adv_opt_domain', attr: 'domain', label: S.domain, default: 'Reals' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_EQUATION);
    this.setTooltip(S.ttSolveIneq);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 解不等式组积木。
  // ---------------------------------------------------------------------------
  registerBlock('solve_inequality_system', function() {
    this.appendDummyInput().appendField(S.solveIneqSys);
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput('x'), 'LHS1')
        .appendField(new Blockly.FieldDropdown(INEQUALITY_OPS), 'OP1')
        .appendField(new Blockly.FieldTextInput('3'), 'RHS1');
    this.appendDummyInput()
        .appendField(new Blockly.FieldTextInput('x'), 'LHS2')
        .appendField(new Blockly.FieldDropdown(INEQUALITY_OPS), 'OP2')
        .appendField(new Blockly.FieldTextInput('1'), 'RHS2');
    addAdvancedSettings(this, [
      { name: 'VAR', optionType: 'adv_opt_var', attr: 'var', label: S.advVar, default: 'x' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_EQUATION);
    this.setTooltip(S.ttSolveIneqSys);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 代数式计算积木。
  // ---------------------------------------------------------------------------
  registerBlock('expr_calc', function() {
    this.appendDummyInput().appendField(S.exprCalc);
    shadowField(this, 'FUNC', S.exprInput, '2+3*4');
    this.setOutput(true, 'String');
    this.setColour(COLOUR_CALC);
    this.setTooltip(S.ttExprCalc);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 解三角形积木。
  // ---------------------------------------------------------------------------
  var TRIANGLE_CONDITIONS = [
    [S.triSelect, ''],
    [S.angA, 'A'], [S.angB, 'B'], [S.angC, 'C'],
    [S.sideA, 'a'], [S.sideB, 'b'], [S.sideC, 'c']
  ];

  registerBlock('solve_triangle', function() {
    this.appendDummyInput().appendField(S.solveTri);
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown(TRIANGLE_CONDITIONS), 'KIND1')
        .appendField(S.value);
    shadowField(this, 'VAL1', '', '');
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown(TRIANGLE_CONDITIONS), 'KIND2')
        .appendField(S.value);
    shadowField(this, 'VAL2', '', '');
    this.appendDummyInput()
        .appendField(new Blockly.FieldDropdown(TRIANGLE_CONDITIONS), 'KIND3')
        .appendField(S.value);
    shadowField(this, 'VAL3', '', '');
    this.setOutput(true, 'String');
    this.setColour(COLOUR_EQUATION);
    this.setTooltip(S.ttSolveTri);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // 调用函数积木：下拉选择已定义的函数，可传入自变量具体值（默认不传入）。
  // ---------------------------------------------------------------------------
  registerBlock('call_func', function() {
    var dropdown = new Blockly.FieldDropdown(
      function() {
        var names = window._blocklyFunctions || [];
        if (names.length === 0) {
          return [[window._blocklyLang === 'en' ? '(no function defined)' : '(未定义函数)', '']];
        }
        return names.map(function(n) { return [n, n]; });
      },
      function(newValue) {
        return newValue;  // 接受所选值；下拉每次打开时自动按最新函数列表刷新
      }
    );
    this.appendDummyInput().appendField(S.callFunc).appendField(dropdown, 'FUNC');
    addAdvancedSettings(this, [
      { name: 'ARG', optionType: 'adv_opt_arg', attr: 'arg', label: S.argVal, default: '' }
    ]);
    this.setOutput(true, 'String');
    this.setColour(COLOUR_CALC);
    this.setTooltip(S.ttCallFunc);
    this.setHelpUrl('');
  });

  // ---------------------------------------------------------------------------
  // Python 生成器
  // ---------------------------------------------------------------------------

  // 两套自定义积木生成器：
  //  - LIBRARY_GENERATORS：调用 CalculusCalculator 库函数（运行按钮始终执行此套）
  //  - NATIVE_GENERATORS ：生成仅依赖 SymPy、可复制到解释器直接运行的自包含代码
  // 通过切换 Blockly.Python.forBlock 中对应条目，在同一工作区上生成两种代码。
  var LIBRARY_GENERATORS = {};
  var NATIVE_GENERATORS = {};

  // 原生模式下"定义函数"积木维护的 原始函数名 -> {pyName, var} 映射
  var nativeFuncMap = {};

  // 将任意字符串转为合法的 Python 标识符（保留中文/字母/数字/下划线）。
  function sanitizePyName(name) {
    var s = String(name == null ? '' : name);
    s = s.replace(/[^A-Za-z0-9_\u4e00-\u9fff]/g, '_');
    if (!/^[A-Za-z_\u4e00-\u9fff]/.test(s)) s = '_' + s;
    return s || '_';
  }

  // 若代码是 JSON 字符串字面量（如 '"x"'），返回其字面值（'x'），否则返回 null。
  function extractStringLiteral(code) {
    if (typeof code === 'string' && code.length >= 2 &&
        code[0] === '"' && code[code.length - 1] === '"') {
      try { return JSON.parse(code); } catch (e) { return null; }
    }
    return null;
  }

  // 轻量读取 value 输入上连接（或 shadow）文本积木的 TEXT 字段值。
  // 与 getEmbeddedInputCode 不同，此函数不经过 valueToCode/blockToCode，
  // 因此可在 CodeGenerator.init() 之前安全调用，避免触发
  // "CodeGenerator init was not called before blockToCode was called" 警告。
  function readEmbeddedText(block, inputName, fallback) {
    var input = block.getInput(inputName);
    var targetBlock = input && input.connection && input.connection.targetBlock();
    if (targetBlock) {
      var val = targetBlock.getFieldValue('TEXT');
      if (val !== null && val !== undefined && val !== '') {
        return String(val);
      }
    }
    return fallback;
  }

  function registerCustomPythonGenerators() {
    // 等待 Blockly.Python 就绪（脚本加载顺序安全，此处仅为兜底）。
    if (!Blockly.Python) {
      setTimeout(registerCustomPythonGenerators, 50);
      return;
    }

    // 库生成器统一挂载到 forBlock（旧版 Blockly 需挂到 Python 对象本身），
    // 同时记录到 LIBRARY_GENERATORS 供模式切换时恢复。
    function registerGenerator(blockType, generatorFn) {
      LIBRARY_GENERATORS[blockType] = generatorFn;
      if (Blockly.Python.forBlock) {
        Blockly.Python.forBlock[blockType] = generatorFn;
      } else {
        Blockly.Python[blockType] = generatorFn;
      }
    }

    // 原生生成器：仅登记到 NATIVE_GENERATORS，由 _blocklyGenerateNativeCode 切换使用。
    function registerNativeGenerator(blockType, generatorFn) {
      NATIVE_GENERATORS[blockType] = generatorFn;
    }

    // 将某套自定义生成器安装到 Blockly.Python（另一套中未覆盖的积木沿用内置生成器）。
    function installGeneratorSet(set) {
      Object.keys(set).forEach(function(k) {
        if (Blockly.Python.forBlock) {
          Blockly.Python.forBlock[k] = set[k];
        } else {
          Blockly.Python[k] = set[k];
        }
      });
    }

    // 生成原生代码前重置跨生成的状态。
    function resetNativeState() {
      nativeFuncMap = {};
    }

    // 读取某个 value 输入对应的代码。
    // 若该输入连接了任意积木（text / math_number / io_input 等，包括默认影子积木），
    // 则通过 valueToCode 生成其代码，尊重用户替换上的积木；
    // 仅当完全没有连接任何积木时才回退到 fallback 默认值。
    function getEmbeddedInputCode(block, inputName, fallbackValue, asNumber) {
      var input = block.getInput(inputName);
      var targetBlock = input && input.connection && input.connection.targetBlock();

      if (targetBlock) {
        var code = Blockly.Python.valueToCode(block, inputName, Blockly.Python.ORDER_NONE);
        if (code) return code;
      }

      if (fallbackValue === null || fallbackValue === undefined) {
        return asNumber ? '0' : "''";
      }
      return asNumber ? String(fallbackValue) : JSON.stringify(String(fallbackValue));
    }

    // 读取内联文本框（FieldTextInput）的值；空字符串时返回 emptyCode（通常是 'None' 或 ''）。
    function inlineText(block, fieldName, emptyCode) {
      var v = block.getFieldValue(fieldName);
      v = (v === null || v === undefined) ? '' : String(v).trim();
      return v === '' ? emptyCode : v;
    }

    // 返回 Python 中的 None（当对应文本为空字符串时）。
    function noneIfEmpty(code) {
      return code === JSON.stringify('') ? 'None' : code;
    }

    // 当表达式/方程输入字段为空字符串时，回退到右侧输入列表中的约定输入。
    // 这是为了支持"在右侧输入区直接维护函数表达式/方程"的用法。
    function resolveFromInputList(code, inputName) {
      if (code !== JSON.stringify('')) return code;
      var inputs = window._blocklyInputs || {};
      var value = inputs[inputName];
      if (value === undefined || value === null || value === '') return code;
      return JSON.stringify(String(value));
    }

    registerGenerator('calc_derivative', function(block) {
      var func = resolveFromInputList(
        getEmbeddedInputCode(block, 'FUNC', 'x**2', false), '函数表达式');
      var order = getEmbeddedInputCode(block, 'ORDER', '1', false);
      var at = getEmbeddedInputCode(block, 'AT', '', false);
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      Blockly.Python.definitions_['import_derivative'] = 'from functions.derivative import derivative';
      return ['derivative(' + func + ', ' + varName + ', ' + order + ', ' + at + ', fs)',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    registerGenerator('calc_integral', function(block) {
      var func = resolveFromInputList(
        getEmbeddedInputCode(block, 'FUNC', 'x**2', false), '函数表达式');
      var lower = inlineText(block, 'LOWER', 'None');
      var upper = inlineText(block, 'UPPER', 'None');
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      Blockly.Python.definitions_['import_integral'] = 'from functions.integral import integral';
      var code = (lower === 'None' && upper === 'None')
        ? 'integral(' + func + ', ' + varName + ', fs)'
        : 'integral(' + func + ', ' + varName + ', fs, ' + lower + ', ' + upper + ')';
      return [code, Blockly.Python.ORDER_FUNCTION_CALL];
    });

    registerGenerator('calc_function_attr', function(block) {
      var attr = block.getFieldValue('ATTR');
      var func = resolveFromInputList(
        getEmbeddedInputCode(block, 'FUNC', 'x**2', false), '函数表达式');
      var domain = inlineText(block, 'DOMAIN', '(-oo, oo)');
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      Blockly.Python.definitions_['import_function_attr'] = 'from functions import get_function_attr';
      return ['get_function_attr(' + func + ', ' + varName + ', ' +
              JSON.stringify(domain) + ', ' + attr + ', fs)',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    registerGenerator('solve_equation', function(block) {
      var eq = resolveFromInputList(
        getEmbeddedInputCode(block, 'EQ', 'x**2-4', false), '方程');
      var domain = inlineText(block, 'DOMAIN', 'Reals');
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      Blockly.Python.definitions_['import_solve_equation'] = 'from functions.solvers import solve_fangcheng';
      return ['solve_fangcheng(' + eq + ', ' + varName + ', ' +
              JSON.stringify(domain) + ', fs)',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    registerGenerator('io_input', function(block) {
      var name = block.getFieldValue('NAME');
      return ['get_input(' + JSON.stringify(name) + ')', Blockly.Python.ORDER_FUNCTION_CALL];
    });

    registerGenerator('io_output', function(block) {
      var name = block.getFieldValue('NAME');
      var value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_NONE) || "''";
      return 'py_output(' + JSON.stringify(name) + ', ' + value + ')\n';
    });

    // 表达式输入积木：直接使用自身文本字段。
    registerGenerator('expr_input', function(block) {
      var text = block.getFieldValue('TEXT');
      return [JSON.stringify(text || ''), Blockly.Python.ORDER_ATOMIC];
    });

    // 定义函数积木：define_func(名称, 表达式, 定义域, 变量)
    registerGenerator('define_func', function(block) {
      var name = inlineText(block, 'NAME', 'f');
      var func = getEmbeddedInputCode(block, 'FUNC', 'x**2', false);
      var domain = getEmbeddedInputCode(block, 'DOMAIN', 'Reals', false);
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      return 'define_func(' + JSON.stringify(name) + ', ' + func + ', ' +
             domain + ', ' + varName + ')\n';
    });

    // 代数式变形积木：py_simplifies(表达式, 方法, 主元, 换元符, 换元式)
    registerGenerator('expr_simplify', function(block) {
      var method = block.getFieldValue('METHOD') || '0';
      var func = getEmbeddedInputCode(block, 'FUNC', 'x**2+2*x+1', false);
      var collect = getEmbeddedInputCode(block, 'COLLECT', 'x', false);
      var subBy = getEmbeddedInputCode(block, 'SUBBY', 't', false);
      var sub = getEmbeddedInputCode(block, 'SUB', '', false);
      return ['py_simplifies(' + func + ', ' + method + ', ' +
              collect + ', ' + subBy + ', ' + sub + ')',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解方程组积木：py_solve_fangchengzu([方程1, 方程2], 变量串)
    registerGenerator('solve_equations', function(block) {
      var eq1 = getEmbeddedInputCode(block, 'EQ1', 'x**2-y', false);
      var eq2 = getEmbeddedInputCode(block, 'EQ2', 'x+y-2', false);
      var vars = getEmbeddedInputCode(block, 'VARS', 'x,y', false);
      return ['py_solve_fangchengzu([' + eq1 + ', ' + eq2 + '], ' + vars + ')',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解不等式积木：py_solve_budengshi(左式, 运算符, 右式, 变量, 定义域)
    registerGenerator('solve_inequality', function(block) {
      var lhs = JSON.stringify(inlineText(block, 'LHS', 'x**2'));
      var rhs = JSON.stringify(inlineText(block, 'RHS', '4'));
      var op = block.getFieldValue('OP') || '>';
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      var domain = getEmbeddedInputCode(block, 'DOMAIN', 'Reals', false);
      return ['py_solve_budengshi(' + lhs + ', ' + JSON.stringify(op) + ', ' +
              rhs + ', ' + varName + ', ' + domain + ')',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解不等式组积木：py_solve_budengshizu([[左,符,右],[左,符,右]], 变量)
    registerGenerator('solve_inequality_system', function(block) {
      function item(lhsName, opName, rhsName) {
        var lhs = JSON.stringify(inlineText(block, lhsName, 'x'));
        var rhs = JSON.stringify(inlineText(block, rhsName, '3'));
        var op = block.getFieldValue(opName) || '>';
        return '[' + lhs + ', ' + JSON.stringify(op) + ', ' + rhs + ']';
      }
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      return ['py_solve_budengshizu([' + item('LHS1', 'OP1', 'RHS1') + ', ' +
              item('LHS2', 'OP2', 'RHS2') + '], ' + varName + ')',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 代数式计算积木：py_calc(表达式)
    registerGenerator('expr_calc', function(block) {
      var func = getEmbeddedInputCode(block, 'FUNC', '2+3*4', false);
      return ['py_calc(' + func + ')', Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解三角形积木：py_solve_triangle([类型,值],[类型,值],[类型,值])
    registerGenerator('solve_triangle', function(block) {
      function cond(kindName, valName) {
        var kind = block.getFieldValue(kindName) || '';
        var val = getEmbeddedInputCode(block, valName, '', false);
        return '[' + JSON.stringify(kind) + ', ' + val + ']';
      }
      return ['py_solve_triangle(' + cond('KIND1', 'VAL1') + ', ' +
              cond('KIND2', 'VAL2') + ', ' + cond('KIND3', 'VAL3') + ')',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 调用函数积木：py_func_value(函数名, 自变量取值或空)
    registerGenerator('call_func', function(block) {
      var name = block.getFieldValue('FUNC') || '';
      var arg = getEmbeddedInputCode(block, 'ARG', '', false);
      return ['py_func_value(' + JSON.stringify(name) + ', ' + arg + ')',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // ---------------------------------------------------------------------------
    // 原生 SymPy 生成器：生成仅依赖 SymPy、可直接复制运行的 Python 代码。
    // 与上面的"库代码"生成器并存；预览时按下拉框切换，运行时始终使用库代码。
    // ---------------------------------------------------------------------------

    // 原生代码前缀：SymPy 导入 + 输入/输出辅助函数 + 定义域转换辅助函数。
    // 仅用于"预览"展示与复制，不参与"运行"（运行走库代码 + PythonBridge）。
    var NATIVE_PRELUDE = [
      '# Generated by CalculusCalculator Blockly: self-contained SymPy code.',
      'from sympy import (sympify, symbols, Symbol, diff, integrate, radsimp,',
      '                   simplify, expand, factor, collect, cancel, apart, trigsimp,',
      '                   expand_trig, powsimp, expand_power_exp, expand_log, logcombine,',
      '                   solve, solveset, Eq, Rel, dsolve, Function, maximum, minimum,',
      '                   Interval, Intersection, Union, oo, imageset, Lambda, periodicity,',
      '                   acos, asin, sin, cos, pi, sqrt, Expr, ImageSet)',
      'from sympy.calculus.util import function_range',
      '',
      'def get_input(input_name):',
      '    return input(f"{input_name}: ")',
      '',
      'def py_output(out_name, value):',
      '    print(f"{out_name}: {value}")',
      '',
      'def _native_domain(d):',
      '    """将 "Reals" / "(-oo, oo)" 等定义域文本转为 SymPy 集合。"""',
      '    d = sympify(d)',
      '    if isinstance(d, (tuple, list)) and len(d) == 2:',
      '        return Interval(d[0], d[1])',
      '    return d',
      ''
    ].join('\n');

    // 函数属性辅助函数（内联自 functions/functions.py，仅依赖 SymPy）。
    var NATIVE_ATTR_HELPERS = [
      'def _native_frange(f, s, d):',
      '    return function_range(sympify(f), symbols(s), domain=d)',
      '',
      'def _native_monotonic_interval(f, s, d, is_increase):',
      '    rel_op = ">" if is_increase else "<"',
      '    return solveset(Rel(diff(sympify(f), symbols(s)), 0, rel_op),',
      '                    symbols(s), domain=d)',
      '',
      'def _native_odd_or_even(f, s, d):',
      '    if Intersection(Interval.open(-oo, 0), d).symmetric_difference(',
      '            imageset(Lambda(symbols(s), -symbols(s)),',
      '                     Intersection(Interval.open(0, oo), d))).is_empty:',
      '        if sympify(f).equals(0):',
      '            return "既奇又偶函数"',
      '        elif sympify(f).equals(-(sympify(f).subs(symbols(s), -symbols(s)))):',
      '            return "奇函数"',
      '        elif sympify(f).equals(sympify(f).subs(symbols(s), -symbols(s))):',
      '            return "偶函数"',
      '        else:',
      '            return "非奇非偶函数"',
      '    else:',
      '        return "非奇非偶函数"',
      '',
      'def _native_period(f, s, d):',
      '    p = periodicity(sympify(f), symbols(s))',
      '    try:',
      '        if d.sup == oo:',
      '            return p if p is not None else "该函数无周期"',
      '        elif d.sup != oo and d == -oo:',
      '            return -p if p is not None else "该函数无周期"',
      '        else:',
      '            return "该函数无周期"',
      '    except Exception:',
      '        return "该函数无周期"',
      '',
      'def _native_mvalues(f, s, d, is_max):',
      '    if is_max:',
      '        return maximum(sympify(f), symbols(s), domain=d)',
      '    return minimum(sympify(f), symbols(s), domain=d)',
      ''
    ].join('\n');

    // 解三角形辅助函数（内联自 functions/solvers.py，仅依赖 SymPy）。
    var NATIVE_TRIANGLE_HELPER = [
      'def _native_solve_triangle(angles, sides):',
      '    """解三角形：angles/sides 为 角名->SymPy表达式 的字典。返回[[角度字典, 边长字典], ...]。"""',
      '    def get_cos(s1, s2, s3):',
      '        return acos((s1**2 + s2**2 - s3**2) / (2 * s1 * s2))',
      '    def rsafe(v):',
      '        try:',
      '            return radsimp(simplify(v))',
      '        except Exception:',
      '            return v',
      '    if len(angles) == 2:',
      '        if list(sides.keys())[0].upper() in angles.keys():',
      '            R = list(sides.values())[0] / sin(angles[list(sides.keys())[0].upper()]) / 2',
      '            other = [a for a in angles.keys() if list(sides.keys())[0].upper() != a][0]',
      '            second_side = 2 * R * sin(angles[other])',
      '            third_angle = pi - list(angles.values())[0] - list(angles.values())[1]',
      '            third_side = 2 * R * sin(third_angle)',
      '            result_angles = angles.copy()',
      '            result_angles[[a for a in ["A", "B", "C"] if a not in list(angles.keys())][0]] = third_angle',
      '            result_sides = sides.copy()',
      '            result_sides[other.lower()] = second_side',
      '            result_sides[[s for s in ["a", "b", "c"] if s not in result_sides.keys()][0]] = third_side',
      '        else:',
      '            third_angle = pi - list(angles.values())[0] - list(angles.values())[1]',
      '            third_side = list(sides.values())[0]',
      '            R = third_side / sin(third_angle) / 2',
      '            result_angles = angles.copy()',
      '            result_angles[[a for a in ["A", "B", "C"] if a not in list(angles.keys())][0]] = third_angle',
      '            result_sides = sides.copy()',
      '            result_sides[list(angles.keys())[0].lower()] = 2 * R * sin(list(angles.values())[0])',
      '            result_sides[list(angles.keys())[1].lower()] = 2 * R * sin(list(angles.values())[1])',
      '        return [[{k: rsafe(v) for k, v in result_angles.items()},',
      '                 {k: rsafe(v) for k, v in result_sides.items()}]]',
      '    elif len(angles) == 1:',
      '        if list(angles.keys())[0].lower() in sides.keys():',
      '            angle_name = list(angles.keys())[0]',
      '            opposite_side = sides[angle_name.lower()]',
      '            other_side_name = [s for s in sides.keys() if s != angle_name.lower()][0]',
      '            other_side = sides[other_side_name]',
      '            angle_val = list(angles.values())[0]',
      '            sin_other = other_side * sin(angle_val) / opposite_side',
      '            if sin_other > 1 + 1e-12:',
      '                return []',
      '            if sin_other > 1:',
      '                sin_other = 1',
      '            if sin_other < -1e-12:',
      '                return []',
      '            other_angle1 = asin(sin_other)',
      '            other_angle2 = pi - other_angle1',
      '            solutions = []',
      '            for other_angle in (other_angle1, other_angle2):',
      '                if other_angle <= 0 or other_angle >= pi:',
      '                    continue',
      '                third_angle = pi - angle_val - other_angle',
      '                if third_angle <= 0:',
      '                    continue',
      '                third_side = opposite_side * sin(third_angle) / sin(angle_val)',
      '                result_angles = angles.copy()',
      '                other_angle_name = other_side_name.upper()',
      '                result_angles[other_angle_name] = other_angle',
      '                third_angle_name = [n for n in ["A", "B", "C"] if n not in result_angles][0]',
      '                result_angles[third_angle_name] = third_angle',
      '                result_sides = sides.copy()',
      '                third_side_name = [s for s in ["a", "b", "c"] if s not in result_sides][0]',
      '                result_sides[third_side_name] = third_side',
      '                solutions.append([{k: rsafe(v) for k, v in result_angles.items()},',
      '                                  {k: rsafe(v) for k, v in result_sides.items()}])',
      '            if len(solutions) == 2 and abs(solutions[0][0][other_angle_name] - solutions[1][0][other_angle_name]) < 1e-12:',
      '                solutions = solutions[:1]',
      '            return solutions',
      '        else:',
      '            third_side = sqrt(list(sides.values())[0]**2 + list(sides.values())[1]**2 - 2*list(sides.values())[0]*list(sides.values())[1]*cos(list(angles.values())[0]))',
      '            result_sides = sides.copy()',
      '            result_sides[list(angles.keys())[0].lower()] = third_side',
      '            result_angles = angles.copy()',
      '            result_angles[list(sides.keys())[0].upper()] = get_cos(list(sides.values())[1], third_side, list(sides.values())[0])',
      '            result_angles[list(sides.keys())[1].upper()] = get_cos(list(sides.values())[0], third_side, list(sides.values())[1])',
      '            return [[{k: rsafe(v) for k, v in result_angles.items()},',
      '                     {k: rsafe(v) for k, v in result_sides.items()}]]',
      '    elif len(angles) == 0:',
      '        result_sides = sides.copy()',
      '        a, b, c = sides["a"], sides["b"], sides["c"]',
      '        result_angles = {"A": get_cos(b, c, a), "B": get_cos(a, c, b), "C": get_cos(a, b, c)}',
      '        return [[{k: rsafe(v) for k, v in result_angles.items()},',
      '                 {k: rsafe(v) for k, v in result_sides.items()}]]',
      '    else:',
      '        return "无解"',
      ''
    ].join('\n');

    // 将辅助函数写入 definitions_（由 finish() 自动前置到生成代码）。
    function provideHelper(key, text) {
      if (!Blockly.Python.definitions_[key]) {
        Blockly.Python.definitions_[key] = text;
      }
    }

    // 求导（原生）：radsimp(diff(sympify(f), symbols(v), int(n))[.subs(...)])
    registerNativeGenerator('calc_derivative', function(block) {
      var func = resolveFromInputList(
        getEmbeddedInputCode(block, 'FUNC', 'x**2', false), '函数表达式');
      var order = getEmbeddedInputCode(block, 'ORDER', '1', false);
      var at = getEmbeddedInputCode(block, 'AT', '', false);
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      var base = 'radsimp(diff(sympify(' + func + '), symbols(' + varName + '), int(' + order + ')))';
      if (at && at !== JSON.stringify('')) {
        return [base + '.subs(symbols(' + varName + '), sympify(' + at + '))',
                Blockly.Python.ORDER_FUNCTION_CALL];
      }
      return [base, Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 积分（原生）：radsimp(integrate(sympify(f), symbols(v)[, (symbols(v), a, b)]))
    registerNativeGenerator('calc_integral', function(block) {
      var func = resolveFromInputList(
        getEmbeddedInputCode(block, 'FUNC', 'x**2', false), '函数表达式');
      var lower = inlineText(block, 'LOWER', 'None');
      var upper = inlineText(block, 'UPPER', 'None');
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      if (lower === 'None' && upper === 'None') {
        return ['radsimp(integrate(sympify(' + func + '), symbols(' + varName + ')))',
                Blockly.Python.ORDER_FUNCTION_CALL];
      }
      return ['radsimp(integrate(sympify(' + func + '), (symbols(' + varName +
              '), sympify(' + JSON.stringify(lower) + '), sympify(' + JSON.stringify(upper) + '))))',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 函数属性（原生）：调用内联的 _native_* 辅助函数
    registerNativeGenerator('calc_function_attr', function(block) {
      var attr = block.getFieldValue('ATTR') || '1';
      var func = resolveFromInputList(
        getEmbeddedInputCode(block, 'FUNC', 'x**2', false), '函数表达式');
      var domain = inlineText(block, 'DOMAIN', '(-oo, oo)');
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      provideHelper('native_attr_helpers', NATIVE_ATTR_HELPERS);
      var fnName, extra = '';
      switch (attr) {
        case '2': fnName = '_native_monotonic_interval'; extra = ', True'; break;
        case '3': fnName = '_native_monotonic_interval'; extra = ', False'; break;
        case '4': fnName = '_native_odd_or_even'; break;
        case '5': fnName = '_native_period'; break;
        case '6': fnName = '_native_mvalues'; extra = ', True'; break;
        case '7': fnName = '_native_mvalues'; extra = ', False'; break;
        default: fnName = '_native_frange'; break;
      }
      return [fnName + '(' + func + ', ' + varName + ', _native_domain(' +
              JSON.stringify(domain) + ')' + extra + ')',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解方程（原生）：solveset(sympify(eq), symbols(v), _native_domain(domain))
    registerNativeGenerator('solve_equation', function(block) {
      var eq = resolveFromInputList(
        getEmbeddedInputCode(block, 'EQ', 'x**2-4', false), '方程');
      var domain = inlineText(block, 'DOMAIN', 'Reals');
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      return ['solveset(sympify(' + eq + '), symbols(' + varName + '), _native_domain(' +
              JSON.stringify(domain) + '))',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 输入（原生）：与库代码一致
    registerNativeGenerator('io_input', function(block) {
      var name = block.getFieldValue('NAME');
      return ['get_input(' + JSON.stringify(name) + ')', Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 输出（原生）：与库代码一致
    registerNativeGenerator('io_output', function(block) {
      var name = block.getFieldValue('NAME');
      var value = Blockly.Python.valueToCode(block, 'VALUE', Blockly.Python.ORDER_NONE) || "''";
      return 'py_output(' + JSON.stringify(name) + ', ' + value + ')\n';
    });

    // 表达式输入（原生）：与库代码一致（纯字符串字面量）
    registerNativeGenerator('expr_input', function(block) {
      var text = block.getFieldValue('TEXT');
      return [JSON.stringify(text || ''), Blockly.Python.ORDER_ATOMIC];
    });

    // 定义函数（原生）：生成 def {name}({var}): return sympify(...).subs(...)
    registerNativeGenerator('define_func', function(block) {
      var name = inlineText(block, 'NAME', 'f');
      var func = getEmbeddedInputCode(block, 'FUNC', 'x**2', false);
      var domain = getEmbeddedInputCode(block, 'DOMAIN', 'Reals', false);
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      var varStr = extractStringLiteral(varName);
      if (varStr === null) varStr = 'x';
      var pyName = sanitizePyName(name);
      var pyVar = sanitizePyName(varStr);
      nativeFuncMap[String(name)] = { pyName: pyName, var: varStr };
      return 'def ' + pyName + '(' + pyVar + '):\n' +
             '    return sympify(' + func + ').subs(symbols(' +
             JSON.stringify(varStr) + '), ' + pyVar + ')\n';
    });

    // 代数式变形（原生）：直接调用 SymPy 化简/展开/因式分解等
    registerNativeGenerator('expr_simplify', function(block) {
      var method = block.getFieldValue('METHOD') || '0';
      var func = getEmbeddedInputCode(block, 'FUNC', 'x**2+2*x+1', false);
      var collect = getEmbeddedInputCode(block, 'COLLECT', 'x', false);
      var subBy = getEmbeddedInputCode(block, 'SUBBY', 't', false);
      var sub = getEmbeddedInputCode(block, 'SUB', '', false);
      var e = 'sympify(' + func + ')';
      var code;
      switch (method) {
        case '1': code = 'expand(' + e + ')'; break;
        case '2': code = 'factor(' + e + ')'; break;
        case '3': code = 'collect(' + e + ', symbols(' + collect + '))'; break;
        case '4': code = 'cancel(' + e + ')'; break;
        case '5': code = 'apart(' + e + ')'; break;
        case '6': code = 'trigsimp(' + e + ')'; break;
        case '7': code = 'expand_trig(' + e + ')'; break;
        case '8': code = 'powsimp(' + e + ')'; break;
        case '9': code = 'expand_power_exp(' + e + ')'; break;
        case '10': code = 'expand_log(' + e + ', force=True)'; break;
        case '11': code = 'logcombine(' + e + ')'; break;
        case '12':
          code = 'expand(' + e + '.subs(symbols(' + collect + '), ' +
                 'solve(Eq(symbols(' + subBy + ', positive=True), sympify(' + sub +
                 ')), symbols(' + collect + '))[0]))';
          break;
        default: code = 'simplify(' + e + ')'; break;
      }
      return ['radsimp(' + code + ')', Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解方程组（原生）：solve([Eq(...), Eq(...)], list(symbols(vars)))
    registerNativeGenerator('solve_equations', function(block) {
      var eq1 = getEmbeddedInputCode(block, 'EQ1', 'x**2-y', false);
      var eq2 = getEmbeddedInputCode(block, 'EQ2', 'x+y-2', false);
      var vars = getEmbeddedInputCode(block, 'VARS', 'x,y', false);
      return ['solve([Eq(sympify(' + eq1 + '), 0), Eq(sympify(' + eq2 + '), 0)], ' +
              'list(symbols(' + vars + ')))',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解不等式（原生）：solveset(Rel(...), symbols(v), _native_domain(domain))
    registerNativeGenerator('solve_inequality', function(block) {
      var lhs = JSON.stringify(inlineText(block, 'LHS', 'x**2'));
      var rhs = JSON.stringify(inlineText(block, 'RHS', '4'));
      var op = block.getFieldValue('OP') || '>';
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      var domain = inlineText(block, 'DOMAIN', 'Reals');
      return ['solveset(Rel(sympify(' + lhs + '), sympify(' + rhs + '), ' +
              JSON.stringify(op) + '), symbols(' + varName + '), _native_domain(' +
              JSON.stringify(domain) + '))',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解不等式组（原生）：solve([Rel, Rel], symbols(v)).as_set()
    registerNativeGenerator('solve_inequality_system', function(block) {
      function item(lhsName, opName, rhsName) {
        var lhs = JSON.stringify(inlineText(block, lhsName, 'x'));
        var rhs = JSON.stringify(inlineText(block, rhsName, '3'));
        var op = block.getFieldValue(opName) || '>';
        return 'Rel(sympify(' + lhs + '), sympify(' + rhs + '), ' + JSON.stringify(op) + ')';
      }
      var varName = getEmbeddedInputCode(block, 'VAR', 'x', false);
      return ['solve([' + item('LHS1', 'OP1', 'RHS1') + ', ' +
              item('LHS2', 'OP2', 'RHS2') + '], symbols(' + varName + ')).as_set()',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 代数式计算（原生）：radsimp(simplify(sympify(f)))
    registerNativeGenerator('expr_calc', function(block) {
      var func = getEmbeddedInputCode(block, 'FUNC', '2+3*4', false);
      return ['radsimp(simplify(sympify(' + func + ')))',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 解三角形（原生）：调用内联的 _native_solve_triangle(角度字典, 边长字典)
    registerNativeGenerator('solve_triangle', function(block) {
      function cond(kindName, valName) {
        var kind = block.getFieldValue(kindName) || '';
        var val = getEmbeddedInputCode(block, valName, '', false);
        return { kind: String(kind).trim(), val: val };
      }
      var conds = [cond('KIND1', 'VAL1'), cond('KIND2', 'VAL2'), cond('KIND3', 'VAL3')];
      var angles = [], sides = [];
      conds.forEach(function(c) {
        if (!c.kind || !c.val || c.val === JSON.stringify('')) return;
        if (/^[A-Z]$/.test(c.kind)) {
          angles.push(JSON.stringify(c.kind) + ': sympify(' + c.val + ')');
        } else if (/^[a-z]$/.test(c.kind)) {
          sides.push(JSON.stringify(c.kind) + ': sympify(' + c.val + ')');
        }
      });
      provideHelper('native_triangle_helper', NATIVE_TRIANGLE_HELPER);
      return ['_native_solve_triangle({' + angles.join(', ') + '}, {' + sides.join(', ') + '})',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // 调用函数（原生）：{pyName}(symbols(var)) 或 {pyName}(sympify(arg))
    registerNativeGenerator('call_func', function(block) {
      var name = block.getFieldValue('FUNC') || '';
      var arg = getEmbeddedInputCode(block, 'ARG', '', false);
      var entry = nativeFuncMap[String(name)] ||
          { pyName: sanitizePyName(name), var: 'x' };
      if (arg && arg !== JSON.stringify('')) {
        return [entry.pyName + '(sympify(' + arg + '))',
                Blockly.Python.ORDER_FUNCTION_CALL];
      }
      return [entry.pyName + '(symbols(' + JSON.stringify(entry.var) + '))',
              Blockly.Python.ORDER_FUNCTION_CALL];
    });

    // ---------------------------------------------------------------------------
    // 模式切换与导出（供 index.html 调用）
    // ---------------------------------------------------------------------------

    // 生成库代码（运行按钮执行此套）。
    window._blocklyGenerateLibraryCode = function(ws) {
      installGeneratorSet(LIBRARY_GENERATORS);
      Blockly.Python.definitions_ = {};
      Blockly.Python.functionNames_ = {};
      return Blockly.Python.workspaceToCode(ws || null);
    };

    // 生成原生 SymPy 代码（预览下拉框默认展示此套），生成后恢复库生成器。
    window._blocklyGenerateNativeCode = function(ws) {
      resetNativeState();
      // 预扫描所有"定义函数"积木，构建 函数名->{pyName, var} 映射，
      // 使"调用函数"积木即使位于"定义函数"之前也能正确引用。
      // 注意：此处只能直接读取积木字段（readEmbeddedText），
      // 不可调用 valueToCode/getEmbeddedInputCode —— 它们会在
      // CodeGenerator.init() 尚未执行（isInitialized 仍为 false）时
      // 触发 "CodeGenerator init was not called..." 警告。
      if (ws) {
        ws.getAllBlocks(false).forEach(function(b) {
          if (b.type === 'define_func') {
            var nm = inlineText(b, 'NAME', 'f');
            var vs = readEmbeddedText(b, 'VAR', 'x') || 'x';
            nativeFuncMap[String(nm)] = { pyName: sanitizePyName(nm), var: vs };
          }
        });
      }
      installGeneratorSet(NATIVE_GENERATORS);
      Blockly.Python.definitions_ = {};
      Blockly.Python.functionNames_ = {};
      var code;
      try {
        code = Blockly.Python.workspaceToCode(ws || null);
      } finally {
        // 无论生成是否成功，都恢复库生成器，保证"运行"始终走库代码。
        installGeneratorSet(LIBRARY_GENERATORS);
      }
      return code;
    };

    // 返回原生代码前缀（预览时拼接到生成代码之前）。
    window._blocklyNativePrelude = function() {
      return NATIVE_PRELUDE;
    };

    // 标记生成器已就绪，供 index.html 等待。
    window._blocklyCustomPythonGeneratorsReady = true;
  }

  registerCustomPythonGenerators();
})();
