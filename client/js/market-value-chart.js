var React = require('react');
var ReactDOM = require('react-dom');
var ScatterChart = require('./scatter-chart');

var MarketValueChart = React.createClass({
    render: function(){
        var data = [];
        this.props.mktvalues.forEach(function(obj){
            var dtStr = obj.date.split('-');
            dtStr[2] = parseInt(dtStr[2]) + 1;
            data.push({x: new Date(dtStr), y: obj.mktvalue}); 
        });

        var chartData = [{
            data: data
        }];

        var options = {
            responsive: true,
            maintainAspectRatio: false,
            scaleShowLabels: true,
            scaleType: 'date',
            scaleTimeFormat: '',
            datasetStrokeColor: 'rgba(151,187,205,1)',
            datasetPointStrokeColor: 'rgba(151,187,205,0.75)'
        };

        return (
            <div className="row">
                <div className="col-xs-12 col-md-8 col-md-offset-2">
                    <ScatterChart data={chartData} 
                                  options={options}
                                  width="800" 
                                  height="400" />
                </div>
            </div>
        );       
    }
});

module.exports = MarketValueChart;
