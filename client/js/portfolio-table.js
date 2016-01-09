var React = require('react');
var ReactDOM = require('react-dom');
var PortfolioCategoryRow = require('./portfolio-category-row');
var formatters = require('./formatters');

var PortfolioTable = React.createClass({
    render: function(){
        var categoryNodes = this.props.categories.map(function(category, idx){
            return (
                <PortfolioCategoryRow category={category} key={idx} />
            );
        });

        return (
            <table className="table">
                <thead>
                    <tr>
                        <th>Category</th>
                        <th className="hidden-xs">Ticker(s)</th>
                        <th className="hidden-xs text-right">Target %</th>
                        <th className="hidden-xs text-right">Current %</th>
                        <th><div className="pull-right">Target $</div></th>
                        <th><div className="pull-right">Market Value</div></th>
                    </tr>
                </thead>
                <tbody>
                {categoryNodes}
                </tbody>
                <tfoot>
                    <tr>
                        <td></td>
                        <td className="hidden-xs"></td>
                        <td className="hidden-xs"></td>
                        <td className="hidden-xs"></td>
                        <td className="text-right">Total Market Value</td>
                        <td className="text-right">{ formatters.money(this.props.total) }</td>
                    </tr>
                </tfoot>
            </table>
        );
    }
});

module.exports = PortfolioTable;
