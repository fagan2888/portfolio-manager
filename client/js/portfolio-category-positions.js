var React = require('react');
var formatters = require('./formatters');
var PortfolioCategoryPositionRow = require('./portfolio-category-position-row');
var PortfolioCategoryActionsRow = require('./portfolio-category-actions-row');

var PortfolioCategoryPositions = React.createClass({
    getInitialState: function(){
        return {
            editMode: false,
            positions: {} 
        };
    },
    onPositionChange: function(position){
        this.state.positions[position.ticker] = position;
        this.setState({positions: this.state.positions}); 
    },
    onSaveClick: function(){
        this.props.savePositions(this.state.positions);
        this.setState({editMode: false});
        this.props.toggleEditMode();
    },
    onEditClick: function(){
        this.setState({editMode: true});
        this.props.toggleEditMode();
    },
    onCancelClick: function(){
        this.setState({editMode: false});
        this.props.toggleEditMode();
    },
    render: function(){
        var positionNodes = this.props.positions.map(function(position, idx){
            return (
                <PortfolioCategoryPositionRow 
                    key={position.ticker}
                    position={position}
                    editMode={this.state.editMode} 
                    onPositionChange={this.onPositionChange} />
            );
        }, this);

        
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
                <PortfolioCategoryActionsRow
                    editMode={this.state.editMode}
                    onEditClick={this.onEditClick}
                    onSaveClick={this.onSaveClick}
                    onCancelClick={this.onCancelClick} />
                </tfoot>
            </table>
        );    
    }
});

module.exports = PortfolioCategoryPositions;
