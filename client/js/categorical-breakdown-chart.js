var React = require('react');
var BarChart = require('react-chartjs').Bar;

var CategoricalBreakdownChart = React.createClass({
    render: function(){
        var chartData = {
            labels: [],
            datasets: [{
                label: "Target %",
                fillColor: "rgba(220,220,220,0.5)",
                strokeColor: "rgba(220,220,220,0.75)",
                highlightFill: "rgba(220,220,220,0.75)",
                highlightStroke: "rgba(220,220,220,1)",
                data: []
            },{
                label: "Actual %",
                fillColor: "rgba(151,187,205,0.5)",
                strokeColor: "rgba(151,187,205,0.8)",
                highlightFill: "rgba(151,187,205,0.75)",
                highlightStroke: "rgba(151,187,205,1)",
                data: []
            }]
        };

        this.props.categories.forEach(function(category){
            chartData.labels.push(category['name']);
            chartData.datasets[0].data.push((category['target%'] * 100).toFixed(2));
            chartData.datasets[1].data.push((category['current%'] * 100).toFixed(2));
        }, this);
        
        var style = {
            maxWidth: '800px',
            maxHeight: '400px',
            display: 'block',
            margin: '0 auto'
        };

        var options = {
            responsive: true,
            maintainAspectRatio: false
        };

        return (
            <div className="row">
                <div className="col-xs-12 col-md-8 col-md-offset-2">
                    <BarChart data={chartData} 
                              options={options}
                              width="800" 
                              height="400" />
                </div>
            </div>
        );
    }
});

module.exports = CategoricalBreakdownChart;
