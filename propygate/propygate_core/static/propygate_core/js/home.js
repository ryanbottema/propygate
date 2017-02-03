
require(['jquery', 'd3'], function($, d3) {
    
    var enviros_data,
        chart_width,
        margin,
        width,
        height,
        svg;
    
    // ajax initial
    $.ajax({
        url: home_vars.get_chart_data_url,
        data: {}
    }).done(function(res_enviros_data) {
        enviros_data = res_enviros_data;
        console.log(enviros_data);
        setup_chart();
    });
    
    function setup_chart() {
        
        chart_width = $('#enviro-chart').width();
        margin = {top: 20, right: 20, bottom: 55, left: 40};
        width = chart_width - margin.left - margin.right;
        height = 600 - margin.top - margin.bottom;
        
        svg = d3.select("#enviro-chart").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    }

    
    

    function update_chart() {

        

    }
    
});