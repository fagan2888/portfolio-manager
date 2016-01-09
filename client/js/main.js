var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery');
var PortfolioHeader = require('./portfolio-header');
var PortfolioTable = require('./portfolio-table')

var AppView = React.createClass({
    getInitialState: function(){
        return portfolio;
    },
    componentDidMount: function(){
        setInterval(this.refresh, this.props.pollInterval);
    },
    refresh: function(){
        $.ajax(this.props.resource, {
            success: function(data){
                this.setState(data.portfolio);
            }.bind(this),
            error: function(){
                // todo
            }
        });

    },
    render: function(){
        return (
            <div>
                <PortfolioHeader usdcad={this.state.usdcad} asof={this.state.asof} />
                <PortfolioTable categories={this.state.categories} positions={this.state.positions} total={this.state.total}/>
            </div>
        );
    }
});

ReactDOM.render(
    <AppView pollInterval={10000} resource='/positions' />,
    document.getElementById('content')
);
