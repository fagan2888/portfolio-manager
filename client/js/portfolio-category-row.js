var React = require('react');
var ReactDOM = require('react-dom');
var formatters = require('./formatters');

var PortfolioCategoryRow = React.createClass({
    render: function(){
        var tickerNodes = this.props.category.tickers.map(function(ticker, idx){
            return (
                <a style={{display:'block'}} target="_blank" href="https://finance.yahoo.com/q?s={ticker}" key={idx}>{ticker}</a>
            );        
        });

        return (
            <tr className="cat { this.props.category.rebalance? 'danger': '' }" data-toggle="collapse" data-target="#catdtl{ this.props.category.key }">
                <td>{ this.props.category.name }</td>
                <td className="hidden-xs">
                    {tickerNodes}
                </td>
                <td className="hidden-xs text-right">{ formatters.pct(this.props.category['target%']) }</td>
                <td className="hidden-xs text-right">{ formatters.pct(this.props.category['current%']) }</td>
                <td className="text-right">{ formatters.money(this.props.category['target']) }</td>
                <td className="text-right">{ formatters.money(this.props.category['mktvalue']) }</td>
            </tr>
        );
    }
});

module.exports = PortfolioCategoryRow;
