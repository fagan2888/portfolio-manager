var React = require('react');
var ReactDOM = require('react-dom');
var $ = require('jquery');
var PortfolioHeader = require('./portfolio-header');
var PortfolioTable = require('./portfolio-table');
var CategoricalBreakdownChart = require('./categorical-breakdown-chart');

var AppView = React.createClass({
    getInitialState: function(){
        return {
            editMode: false,
            asof: portfolio.asof,
            usdcad: portfolio.usdcad,
            categories: portfolio.categories,
            positions: portfolio.positions,
            total: portfolio.total
        };
    },
    componentDidMount: function(){
        setInterval(this.refresh, this.props.pollInterval);
    },
    refresh: function(){
        if(!document.hidden && !this.state.editMode){
            $.ajax(this.props.resource, {
                success: function(data){
                    this.setState(data.portfolio);
                }.bind(this),
                error: function(){
                    // todo
                }
            });
        }
    },
    toggleEditMode: function(){
        this.setState({editMode: !this.state.editMode});
    },
    savePositions: function(positions){    
        for(var ticker in positions){
            this.state.positions[ticker].qty = positions[ticker].qty;
        }

        $.ajax(this.props.resource, {
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                positions: this.state.positions
            }),
            success: this.refresh
        });

        // remove any zero quantity entries from state
        for(var ticker in this.state.positions){
            if(this.state.positions[ticker].qty === 0){
                delete this.state.positions[ticker];
            }
        }

        this.setState({positions: this.state.positions});
    },
    render: function(){
        return (
            <div>
                <PortfolioHeader usdcad={this.state.usdcad} 
                                 asof={this.state.asof} />        
                <CategoricalBreakdownChart 
                    categories={this.state.categories} 
                    categoryColors={this.state.categoryColors} />
                <PortfolioTable categories={this.state.categories} 
                                positions={this.state.positions} 
                                total={this.state.total}
                                savePositions={this.savePositions} 
                                toggleEditMode={this.toggleEditMode} />
            </div>
        );
    }
});

ReactDOM.render(
    <AppView pollInterval={10000} resource='/positions' />,
    document.getElementById('content')
);
