var React = require('react');

var PortfolioCategoryActionsRow = React.createClass({
    render: function(){
        var actions = (
            <tr>
                <td colSpan="3">
                    <button className="btn btn-success pull-right"
                            onClick={this.props.onEditClick}>
                        Edit
                    </button>
                </td>
            </tr>
        );

        if(this.props.editMode){
            actions = (
                <tr>
                    <td colSpan="3">
                        <button style={{marginLeft: '5px'}} 
                                onClick={this.props.onCancelClick} 
                                className="btn btn-success pull-right">
                            Cancel
                        </button>
                        <button className="btn btn-success pull-right"
                                onClick={this.props.onSaveClick}>
                            Save
                        </button>
                    </td>
                </tr>
            );
        }    
        return actions;
    }
});

module.exports = PortfolioCategoryActionsRow;
