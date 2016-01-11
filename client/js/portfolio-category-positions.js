var React = require('react');
var formatters = require('./formatters');


var PortfolioCategoryPositions = React.createClass({
    getInitialState: function(){
        return {editMode: false};
    },
    onEditClick: function(){
        this.setState({editMode: true});
    },
    onCancelClick: function(){
        this.setState({editMode: false});
    },
    render: function(){
        var positionNodes = this.props.positions.map(function(position, idx){
            var qtyNode = <td className="text-right">{position.qty}</td>;

            if(this.state.editMode){
                qtyNode = <td><input style={{marginBottom: '5px'}} type="text" defaultValue={position.qty} className="pull-right text-right form-control" /></td>; 
            }

            return (
                <tr key={idx}>
                    <td>{position.ticker}</td>
                    {qtyNode}
                    <td className="text-right">{formatters.money(position.mktvalue)}</td>
                </tr>
            );
        }, this);

        var actions = (
            <tr>
                <td colSpan="3">
                    <button onClick={this.onEditClick} className="btn btn-success pull-right">Edit</button>
                </td>
            </tr>
        );

        if(this.state.editMode){
            actions = (
                <tr>
                    <td colSpan="3">
                        <button style={{marginLeft: '5px'}} onClick={this.onCancelClick} className="btn btn-success pull-right">Cancel</button>
                        <button className="btn btn-success pull-right">Save</button>
                    </td>
                </tr>
            );
        }

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
                <tfoot>
                {actions}
                </tfoot>
            </table>
        );    
    }
});

module.exports = PortfolioCategoryPositions;
