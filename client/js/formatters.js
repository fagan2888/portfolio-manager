module.exports = {
    money: function(val){
        return val.toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
    },
    pct: function(val){
        return (val * 100).toFixed(2) + '%';
    },
    dt: function(val){
        return (new Date(val * 1000)).toString();    
    }
};

