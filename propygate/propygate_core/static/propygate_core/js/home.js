
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
        heater_area,
        mainClip,
        maxY,
        minY,
        x_axis_elem,
        y_axis_elem,
        enviro,
        enviro_temps,
        enviro_lights,
        enviro_heater,
        heater_clip,
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
                update_chart();
                update_current_state();
            }
        });
    }

    function update_current_state() {

        for (var env in enviros_data) {

            var enviro_data = enviros_data[env];
            var env_id = enviro_data.id;
            if (enviro_data.temp_data && enviro_data.temp_data.length > 0) {
                $('#current-temp-' + env_id).text(enviro_data.temp_data[enviro_data.temp_data.length - 1].temperature);
            }
            if (enviro_data.ideals && enviro_data.ideals.length > 0) {
                $('#ideal-temp-' + env_id).text(enviro_data.ideals[enviro_data.ideals.length - 1].temp_ideal);
            }
            if (enviro_data.heater_data && enviro_data.heater_data.length > 0) {
                $('#heater-is-' + env_id).text(enviro_data.heater_data[enviro_data.heater_data.length - 1].is_on ? 'On' : 'Off');
                $('#heater-toggle-' + env_id).text(enviro_data.heater_data[enviro_data.heater_data.length - 1].is_on ? 'Turn Off' : 'Turn On');
            }
            if (enviro_data.light_data && enviro_data.light_data.length > 0) {
                $('#light-is-' + env_id).text(enviro_data.light_data[enviro_data.light_data.length - 1].is_on ? 'On' : 'Off');
                $('#light-toggle-' + env_id).text(enviro_data.light_data[enviro_data.light_data.length - 1].is_on ? 'Turn Off' : 'Turn On');
            }

        }

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
        
        heater_area = d3.area()
            .x(function(d) { return xScale(d.x); })
            .y0(function(d) { return yScale(d.temperature) + 8; })
            .y1(function(d) { return yScale(d.temperature) - 8; });
            // .y(function(d) { return yScale(d.temperature); } );
            // .defined(function(d) { return d.is_on; });
        
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

        // heater_clip = enviro.append("defs").append("clipPath").attr('class', 'heater-clip');
        enviro.each(function(d) {
            d3.select('defs').append("clipPath")
                .attr('class', 'heater-clip')
                .attr("id", function() { return 'heater-clip-' + d.id; })
                .append("path")
                    .attr("d", function() { return heater_area(d.temp_data); });
        });

        enviro_heater = enviro.append('g')
            .attr("class", "enviro-heater")
            .attr("clip-path", function(d) { return 'url(#heater-clip-' + d.id + ')'; });
        
        enviro_heater.append('path')
            .attr("class", "area heater")
            .style("pointer-events", "none") // Stop line interferring with cursor
            .attr("id", function(d) {
                return "area_enviro_heater_" + d.id;
            })
            .attr("d", function(d) {
                return light_area(d.heater_data);
            })
            // .attr("clip-path", function(d) { return 'url(#heater-clip-' + d.id + ')'; })//use clip path to make irrelevant part invisible
            .style("fill", function(d) { return d.colour; })
            .style('opacity', 0.3);

        mouse_tracker = svg.append("rect")
            .attr("width", width)
            .attr("height", height)
            .attr("id", "mouse-tracker")
            .style("fill", 'transparent')
            // .on("mousemove", mousemove)
            // .on('click', toggleLock);
    }

    // function find_highest_y(x, y, enviro_id) {
    //     var nodePath = d3.select('path#line_enviro_temps_' + enviro_id);
    //     var best;
    //     for (var highest_y = y + 7; highest_y - y < 100; highest_y += 4) {
    //         best = closestPoint(nodePath, [x, highest_y]);
    //         if (best.distance > 6) {
    //             console.log('-----------------------');
    //             console.log([x, y], [best[0], best[1]], best.distance);
    //             return best[1];
    //         }
    //     }
    //     console.log('None found!');
    //     return best[1]
    // }
    // function find_lowest_y(x, y, enviro_id) {
    //     var nodePath = d3.select('path#line_enviro_temps_' + enviro_id);
    //     for (var lowest_y = y - 7; y - lowest_y < 100; lowest_y -= 4) {
    //         var best = closestPoint(nodePath, [x, lowest_y]);
    //         if (best.distance > 6) {
    //             console.log(best);
    //             return best[1];
    //         }
    //     }
    // }
    // function closestPoint(pathNode, point) {
    //     // console.log(pathNode[0][0]);
    //     var pathLength = pathNode.node().getTotalLength(),
    //         precision = 8,
    //         best,
    //         bestLength,
    //         bestDistance = Infinity;
    //
    //     // linear scan for coarse approximation
    //     for (var scan, scanLength = 0, scanDistance; scanLength <= pathLength; scanLength += precision) {
    //         if ((scanDistance = distance2(scan = pathNode.node().getPointAtLength(scanLength))) < bestDistance) {
    //             best = scan, bestLength = scanLength, bestDistance = scanDistance;
    //         }
    //     }
    //
    //     // binary search for precise estimate
    //     precision /= 2;
    //     while (precision > 0.5) {
    //         var before,
    //             after,
    //             beforeLength,
    //             afterLength,
    //             beforeDistance,
    //             afterDistance;
    //         if ((beforeLength = bestLength - precision) >= 0 && (beforeDistance = distance2(before = pathNode.node().getPointAtLength(beforeLength))) < bestDistance) {
    //             best = before, bestLength = beforeLength, bestDistance = beforeDistance;
    //         } else if ((afterLength = bestLength + precision) <= pathLength && (afterDistance = distance2(after = pathNode.node().getPointAtLength(afterLength))) < bestDistance) {
    //             best = after, bestLength = afterLength, bestDistance = afterDistance;
    //         } else {
    //             precision /= 2;
    //         }
    //     }
    //
    //     best = [best.x, best.y];
    //     best.distance = Math.sqrt(bestDistance);
    //     return best;
    //     // return Math.sqrt(bestDistance);
    //
    //     function distance2(p) {
    //         var dx = p.x - point[0],
    //             dy = p.y - point[1];
    //         return dx * dx + dy * dy;
    //     }
    // }

    d3.select(window).on('resize', function() {
        update_chart();
    });

    go_ajax();
    setInterval(go_ajax, 1000 * 60 * refresh_mins);
    
    $('.relay-btn').click(function() {
        var btn = $(this);
        var relay_id = btn.attr('data-relay-id');
        btn.prop('disabled', true);
        
        $.ajax({
            url: home_vars.toggle_relay_url,
            method: 'POST',
            data: {relay_id: relay_id}
        }).done(function (res_enviros_data) {
            go_ajax();
            btn.prop('disabled', false);
        });
    });

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