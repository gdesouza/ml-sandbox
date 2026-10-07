const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const {test} = require('node:test');
const vm = require('node:vm');
const source = readFileSync('app/static/app.js', 'utf8');

for (const outputId of ['prediction', 'participant-prediction']) {
  test(`${outputId} matches reference diagrams to action probabilities`, () => {
    function node(tag) {
      return {tag, children:[], append(...children) { this.children.push(...children); },
        replaceChildren(...children) { this.children = children; },
        setAttribute(name, value) { this[name] = value; }};
    }
    const output = node('div');
    const context = vm.createContext({
      experiment:{steps:[{action_id:'fold', image:'fold.jpg'}]},
      document:{createElement:node}, $:() => output,
      actionTitle:id => id,
      t:(key, values = {}) => key.replace('{action}', values.action || ''),
      text:(tag, value, className) => Object.assign(node(tag), {textContent:value, className}),
    });
    vm.runInContext(source.slice(source.indexOf('function renderPrediction('), source.indexOf("action('predict',")), context);
    const result = {prediction:{action_id:'fold'}, source:'active', model_version:'v1',
      probabilities:[{action_id:'fold', probability:0.8}, {action_id:'unknown', probability:0.2}]};
    context.renderPrediction(outputId, result);
    const row = output.children[2];
    assert.equal(row.children[0].src, '/static/instructions/fold.jpg');
    assert.equal(row.children[0].alt, 'Diagram for fold');
    assert.equal(row.children[1].children[1].value, 0.8);
    assert.equal(output.children[3].children.length, 1);
    context.actionTitle = () => 'Dobre';
    context.renderPrediction(outputId, result);
    assert.equal(output.children[2].children[0].alt, 'Diagram for Dobre');
  });
}
