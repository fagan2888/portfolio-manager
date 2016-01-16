var React = require('react');
var ReactDOM = require('react-dom');

var ScatterChart = React.createClass({
    renderChart: function(){
        var el = ReactDOM.findDOMNode(this);
        var ctx = el.getContext('2d');
        var ScatterChart = require('chart.js-scatter');
        var Chart = require('chart.js');
        new Chart(ctx).Scatter(this.props.data, this.props.options);
    },
    componentDidMount: function(){
        this.renderChart();
    },
    componentWillUnmount: function(){
        this.state.chart.destroy();
    },
    render: function(){
        return React.createElement('canvas', this.props);
    }
});

module.exports = ScatterChart;
