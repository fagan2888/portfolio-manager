var React = require('react');
var formatters = require('./formatters');


var PortfolioCategoryPositions = React.createClass({
    render: function(){
        var positionNodes = this.props.positions.map(function(position, idx){
            return (
                <tr key={idx}>
                    <td>{position.ticker}</td>
                    <td className="text-right">{position.qty}</td>
                    <td className="text-right">{formatters.money(position.mktvalue)}</td>
                </tr>
            );
        });

        return (    
            <table style={{width:'100%'}}>
                <thead>
                    <tr>
                        <th>Ticker</th>
                        <th className="text-right">Quantity</th>
                        <th className="text-right">Market Value</th>
                    </tr>
                </thead>
                <tbody>
                {positionNodes}
                </tbody>
            </table>
        ); 
    }
});

module.exports = PortfolioCategoryPositions;
