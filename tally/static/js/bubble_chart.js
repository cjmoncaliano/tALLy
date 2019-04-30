
var bubbleChart = function () {
    var width = 600
    height = 400;
    function chart(selection){
        // we gonna get here
    }

    chart.width = function(value) {
        if (!arguments.length) { return width; }
        width = value;

        return chart;
    }
    chart.height = function(value) {
        if (!arguments.length) { return height; }
        height = value;

        return chart;
    }

    return chart;
}
