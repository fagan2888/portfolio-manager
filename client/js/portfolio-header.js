var React = require('react');
var ReactDOM = require('react-dom')
var formatters = require('./formatters')

var PortfolioHeader = React.createClass({
    render: function() {
        return (
           <div className="row">
                <div className="col-xs-6">
                    <p>1 USD = {this.props.usdcad} CAD</p>
                </div>
                <div className="col-xs-6">
                    <p className="pull-right">As Of { formatters.dt(this.props.asof) }</p>
                </div>
            </div>       
        );    
    }
});

module.exports = PortfolioHeader;
