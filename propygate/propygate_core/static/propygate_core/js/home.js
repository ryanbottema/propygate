
require(['jquery', 'd3', 'moment'], function($, d3, moment) {
    
    var num_enviros,
        enviros_data,
        chart_width,
        margin,
        width,
        height,
        svg,
        attrs,
        xScale,
        yScale,
        xAxis,
        yAxis,
        temp_record_line,
        ideal_temp_line,
        light_area,
        mainClip,
        maxY,
        minY,
        x_axis_elem,
        y_axis_elem,
        enviro,
        enviro_temps,
        enviro_lights,
        enviro_heater,
        mouse_tracker,
        refresh_mins = 0.5;
    
    var num_records = 0;
    function go_ajax() {
        $.ajax({
            url: home_vars.get_chart_data_url,
            data: {num_records: num_records}
        }).done(function (res_enviros_data) {
            console.log(res_enviros_data);
            if (!res_enviros_data.changed) {
                num_records = res_enviros_data.num_records;
            } else {
                num_records = res_enviros_data.num_records;
                enviros_data = res_enviros_data.enviros_data;
                num_enviros = enviros_data.length;
                var colours = ['#001F3F', '#D81B60', '#605ca8', '#d2d6de', '#f56954', '#f39c12', '#00c0ef', '#3c8dbc'];
                for (var ed in enviros_data) {
                    enviros_data[ed].colour = colours.pop();
                }
                console.log(enviros_data);
                update_chart();
            }
        });
    }
    
    function update_chart() {

        d3.select("svg").remove();
        
        chart_width = $('#enviro-chart').width();
        margin = {top: 20, right: 20, bottom: 55, left: 40};
        width = chart_width - margin.left - margin.right;
        height = 600 - margin.top - margin.bottom;

        attrs = {
            line_width: 1.5,
            light_stroke_width: 1
        };
        
        svg = d3.select("#enviro-chart").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
              .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        mainClip = svg.append("defs")
            .append("clipPath")
                .attr("id", "clip")
            .append("rect")
                .attr("width", width)
                .attr("height", height);

        xScale = d3.scaleTime().range([0, width]);
        yScale = d3.scaleLinear().range([height, 0]);
        xScale.domain([moment().subtract({hours: 24}).valueOf(), moment().valueOf()]);
        maxY = findMaxY(enviros_data);
        minY = findMinY(enviros_data);
        yScale.domain(yBuff(minY, maxY));
        xAxis = d3.axisBottom(xScale);
        yAxis = d3.axisLeft(yScale);
        yAxis.tickSizeInner(-width).tickSizeOuter(0);

        temp_record_line = d3.line()
            .curve(d3.curveLinear)
            .x(function(d) { return xScale(d.x); })
            .y(function(d) { return yScale(d.temperature); })
            .defined(function(d) { return d.temperature != null; });

        light_area = d3.area()
            .x(function(d) { return xScale(d.x); })
            .y0(function(d) { return 3; })
            .y1(function(d) { return height - 3; })
            .defined(function(d) { return d.is_on; });

        x_axis_elem = svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        y_axis_elem = svg.append("g")
                .attr("class", "y axis")
                // .attr("transform", "translate(" + 0 + "," + 0 + ")")
                .call(yAxis);

        y_axis_elem.append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("x", -10)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Temperature");

        enviro = svg.selectAll(".enviro")
                .data(enviros_data)
            .enter()
                .append("g")
                    .attr("class", "enviro");

        enviro_temps = enviro.append("g")
            .attr("class", "enviro-temps");

        enviro_temps.append("path")
            .attr("class", "line enviro_temps")
            .style("pointer-events", "none") // Stop line interferring with cursor
            .attr("id", function(d) {
                return "line_enviro_temps_" + d.id;
            })
            .attr("d", function(d) {
                return temp_record_line(d.temp_data);
            })
            .attr("clip-path", "url(#clip)")//use clip path to make irrelevant part invisible
            .attr('stroke-width', attrs.line_width)
            .style("stroke", function(d) { return d.colour; });

        enviro_lights = enviro.append('g')
            .attr("class", "enviro-lights");

        enviro_lights.append('path')
            .attr("class", "area lights")
            .style("pointer-events", "none") // Stop line interferring with cursor
            .attr("id", function(d) {
                return "area_enviro_lights_" + d.id;
            })
            .attr("d", function(d) {
                return light_area(d.light_data);
            })
            // .attr("clip-path", "url(#clip)")//use clip path to make irrelevant part invisible
            .style("fill", function(d) { return 'rgba(255, 255, 255, 0.6)'; })
            .style('stroke', function(d) { return d.colour; })
            .style("stroke-dasharray", ("3, 3"))
            .style('stroke-width', attrs.light_stroke_width + 'px');
            // .style('opacity', 0.4);

        enviro_heater = enviro.append('g')
            .attr("class", "enviro-heater");
        
        enviro_heater.append('path')
            .attr("class", "area heater")
            .style("pointer-events", "none") // Stop line interferring with cursor
            .attr("id", function(d) {
                return "area_enviro_heater_" + d.id;
            })
            .attr("d", function(d) {
                return light_area(d.heater_data);
            })
            // .attr("clip-path", "url(#clip)")//use clip path to make irrelevant part invisible
            .style("fill", function(d) { return d.colour; })
            .style('opacity', 0.2);

        mouse_tracker = svg.append("rect")
            .attr("width", width)
            .attr("height", height)
            .attr("id", "mouse-tracker")
            .style("fill", 'transparent')
            // .on("mousemove", mousemove)
            // .on('click', toggleLock);
    }

    d3.select(window).on('resize', function() {
        update_chart();
    });

    go_ajax();
    setInterval(go_ajax, 1000 * 60 * refresh_mins);

    function findMaxY(data) {
        var maxYValues = data.map(function(d) {

            var maxYtd = null;
            if (d.temp_data) {
                maxYtd = d3.max(d.temp_data, function (value) {
                    return value.temperature;
                });
            }
            var maxYi = null;
            if (d.ideals) {
                maxYi = d3.max(d.ideals, function (value) {
                    return value.temp_ideal;
                });
            }
            return d3.max([maxYtd, maxYi]);
        });

        return d3.max(maxYValues) || 0;
    }

    function findMinY(data) {
        var minYValues = data.map(function(d) {

            var minYtd = null;
            if (d.temp_data) {
                minYtd = d3.min(d.temp_data, function (value) {
                    return value.temperature;
                });
            }
            var minYi = null;
            if (d.ideals) {
                minYi = d3.min(d.ideals, function (value) {
                    return value.temp_ideal;
                });
            }
            return d3.min([minYtd, minYi]);
        });

        return d3.min(minYValues) || 0;
    }

    function yBuff(minY, maxY) {
        var y_buff = (maxY - minY) * 0.1;
        return [minY - y_buff, maxY + y_buff];
    }
    
});