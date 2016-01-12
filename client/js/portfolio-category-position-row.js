var React = require('react');
var formatters = require('./formatters');

var PortfolioCategoryPositionRow = React.createClass({
    onQuantityChange: function(){
        this.props.onPositionChange({
            ticker: this.props.position.ticker,
            qty: parseFloat(this.refs.qty.value)
        });    
    },
    render: function(){
        var qtyNode = (
            <td className="text-right">
            {this.props.position.qty}
            </td>
        );

        if(this.props.editMode){
            qtyNode = (
                <td>
                    <input style={{marginBottom: '5px'}} 
                           type="text"
                           ref="qty" 
                           defaultValue={this.props.position.qty} 
                           onChange={this.onQuantityChange}
                           className="pull-right text-right form-control" />
                </td>
            ); 
        }

        return (
            <tr>
                <td>{this.props.position.ticker}</td>
                {qtyNode}
                <td className="text-right">
                    {formatters.money(this.props.position.mktvalue)}
                </td>
            </tr>
        );
    }
});

module.exports = PortfolioCategoryPositionRow;
