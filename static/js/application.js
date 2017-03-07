function double_check(elem) {
    var msg = "Are you sure?";
    var emsg = $(elem).data("confirm");
    if(emsg != undefined && emsg != "") {
        msg = emsg
    }
    if(confirm(msg)) {
        return true;
    }
    return false;
}

function create_customer(elem) {
    var elem = $(elem);
    var url = elem.attr("post-url");
    $("#create-customer-modal").unbind("shown.bs.modal");
    $("#create-customer-modal").on("shown.bs.modal", function() {
        $("#create-customer-name").val("").focus();
        $("#create-customer-servers").val(1);
        $("#create-customer-bandwidth").val(4);
    });
    $("#create-customer-submit").unbind("click");
    $("#create-customer-submit").click(function() {
        var name = $("#create-customer-name").val();
        var servers = $("#create-customer-servers").val();
        var bandwidth = $("#create-customer-bandwidth").val();
        var password = $("#create-customer-password").val();
        var expire = $("#create-customer-expire").val();
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'name': name, 'servers': servers, 'bandwidth': bandwidth, 'password': password, 'expire': expire}),
            statusCode: {
                200: function() {
                    window.location.reload(true);
                },
                400: function(data, text) {
                    alert(data.responseText);
                }
            }
        });
    });
    $("#create-customer-modal").modal('show');
    return false;
}

function edit_customer(elem) {
    var elem = $(elem);
    var emodal = $("#edit-customer-modal");
    var pfx = "#edit-customer-";
    emodal.unbind("shown.bs.modal");
    emodal.on("shown.bs.modal", function() {
        $(pfx+"servers").val(elem.data("servers"));
        $(pfx+"bandwidth").val(elem.data("bandwidth")).focus();
        $(pfx+"expire").val(elem.data("expire"));
        var server_ids = elem.data("serverIds") + "";
        if (server_ids) {
            var server_arr = server_ids.split(",");
            $(pfx+"server-list").val(server_arr);
        }
    });
    $(pfx+"submit").unbind("click");
    $(pfx+"submit").click(function() {
        var url = "/admin/customers/" + elem.data("id") + "/edit";
        var servers = $(pfx+"servers").val();
        var bandwidth = $(pfx+"bandwidth").val();
        var password = $(pfx+"password").val();
        var expire = $(pfx+"expire").val();
        var server_ids = $(pfx+"server-list").val();
        var server_ids_str = server_ids.join(",");
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'servers': servers, 'bandwidth': bandwidth, 'password': password, 'expire': expire, 'server_list': server_ids_str}),
            statusCode: {
                200: function() {
                    window.location.reload(true);
                },
                400: function(data, text) {
                    alert(data.responseText);
                }
            }
        });
    });
    emodal.modal("show");
}

function create_server(elem) {
    var elem = $(elem);
    var url = elem.attr("post-url");
    var emodal = $("#server-modal");
    $("#server-modal-title").html(emodal.data("msgcreate"));
    emodal.unbind("show.bs.modal");
    emodal.unbind("shown.bs.modal");
    emodal.on("show.bs.modal", function() {
        var elem_list = ["#server-hostname", "#server-ip", "#server-comments"]
        for(eid in elem_list) {
            var ielem = $(elem_list[eid]);
            ielem.val("")
            ielem.parent().parent().removeClass("has-error");
        }
        $("#server-port").val("8387");
        $("#server-status").val("Enabled");
        $("#server-encryption").val("aes-128-cfb");
        $("#server-hostname").focus();
    });
    $("#server-modal-submit").unbind("click");
    $("#server-modal-submit").click(function() {
        var hostname = $("#server-hostname").val();
        var ip = $("#server-ip").val();
        var comments = $("#server-comments").val();
        var encryption = $("#server-encryption").val();
        var status = $("#server-status").val();
        var port = $("#server-port").val();
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'hostname': hostname, 'ip': ip, 'comments': comments, 'encryption': encryption, 'status': status, 'port': port}),
            statusCode: {
                200: function() {
                    window.location.reload(true);
                },
                400: function(data, text) {
                    render_error(data, "#server-");
                }
            }
        })
    });
    emodal.modal('show');
}

function change_password() {
    var emodal = $("#change-password-modal");
    emodal.unbind("shown.bs.modal");
    emodal.on("shown.bs.modal", function() {
        $("#change-password-password").val("").focus();
        $("#change-password-confirm").val("");
    });
    $("#change-password-submit").unbind("click");
    $("#change-password-submit").click(function() {
        var password = $("#change-password-password").val();
        var confirm = $("#change-password-confirm").val()
        $.ajax({
            async: false,
            type: "POST",
            url: "/admin/change_password",
            data: add_csrf_token({'password': password, 'confirm': confirm}),
            statusCode: {
                200: function() {
                    window.location.reload(true);
                },
                400: function(data, text) {
                    render_error(data, "#change-password-");
                }
            }
        })
    });
    emodal.modal('show');
}

function edit_server(elem) {
    var elem = $(elem);
    var url = elem.attr("post-url");
    var sid = elem.data("id");
    var emodal = $("#server-modal");
    var can_show = true;
    $("#server-modal-title").html(emodal.data("msgedit"));
    $.ajax({
        async: false,
        type: "GET",
        url: "/admin/servers/"+sid,
        statusCode: {
            200: function(data, text) {
                for(k in data) {
                    var key = "#server-" + k;
                    var value = data[k];
                    var ielem = $(key);
                    ielem.val(value);
                    ielem.parent().parent().removeClass("has-error");
                }
            },
            400: function(data, text) {
                can_show = false;
            }
        }
    });
    emodal.unbind("show.bs.modal");
    emodal.unbind("shown.bs.modal");
    emodal.on("shown.bs.modal", function() {
        $("#server-hostname").focus();
    });
    $("#server-modal-submit").unbind("click");
    $("#server-modal-submit").click(function() {
        var hostname = $("#server-hostname").val();
        var ip = $("#server-ip").val();
        var comments = $("#server-comments").val();
        var encryption = $("#server-encryption").val();
        var status = $("#server-status").val();
        var port = $("#server-port").val();
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'hostname': hostname, 'ip': ip, 'comments': comments, 'encryption': encryption, 'status': status, 'port': port}),
            statusCode: {
                200: function() {
                    window.location.reload(true);
                },
                400: function(data, text) {
                    render_error(data, "#server-");
                }
            }
        })
    });
    if(can_show) emodal.modal('show');
}


function render_customer_modal(elem) {
    var pfx = "#customer-detail-";
    $(pfx+"username").html(elem.data("name"));
    $(pfx+"userid").html(elem.data("userid"));
    var status = elem.data('status');
    var status_html = '<span class="badge bg-green">'+status+'</span>';
    if (status != "Enabled") {
        status_html = '<span class="badge bg-red">'+status+'</span>';
    }
    $(pfx+"status").html(status_html);
    $(pfx+"password").html(elem.data("password"));
    $(pfx+"created-at").html(elem.data("created_at"));
    $.ajax({
        async: false,
        type: "GET",
        url: "/admin/customers/" + elem.data("id"),
        statusCode: {
            200: function(data) {
                var servers_html = "";
                var msg = $(pfx+"servers").data("msg");
                for (var i in data['servers']) {
                    var item = data['servers'][i];
                    servers_html += '<div><span>' + item[0].toUpperCase() + '&nbsp;(' + item[1] + ')</span><span style="min-width:100px;padding-left:5px;">' + msg + ': ' + item[2].toUpperCase() + '</span></div>';
                }
                $(pfx+"servers").html(servers_html);
                var css = "text-green";
                if (data["is_expire"]) {
                    css = "text-red";
                }
                $(pfx+"expire").html("");
                $(pfx+"expire").html(data["expire"]).attr("class", css);
            }
        }
    });
}

function render_total_bandwidth_chart(chart_elem) {
    var url = "/admin/total_bandwidth";
    $.ajax({
        type: "GET",
        url: url,
        statusCode: {
            200: function(data) {
                render_bandwidth_chart(data, chart_elem);
            }
        }
    });
}

function render_customer_modal_chart(elem) {
    var pfx = "#customer-detail-";
    var chart_elem = $(pfx+"bandwidth-chart");
    chart_elem.html("");
    var url = "/api/statistic/bandwidth?userid=" + elem.data('userid');
    $.ajax({
        type: "GET",
        url: url,
        statusCode: {
            200: function(data) {
                render_bandwidth_chart(data, pfx+"bandwidth-chart");
            }
        }
    });
    url = "/api/statistic/connection?userid=" + elem.data('userid');
    $.ajax({
        type: "GET",
        url: url,
        statusCode: {
            200: function(data) {
                render_connection_chart(data, pfx+"connection-chart");
            }
        }
    });
}

function merge(obja, objb) {
    var ret = {};
    for (var k in obja) {
        ret[k] = obja[k];
    }
    for (var k in objb) {
        ret[k] = objb[k];
    }
    return ret;
}

function calculate_interval(data_length) {
    return Math.round(data_length / 5);
}


function tooltip_format_unit(data, unit, step) {
    var ret = '<b>' + data.points[0].key + '</b>';
    $.each(data.points, function () {
        ret += '<br/>' + this.series.name + ': ';
        ret += format_number_by_step(this.y, unit, step);
    });
    return ret;
}

function tooltip_format_connection(data) {
    var ret = '<b>' + data.points[0].key + '</b>';
    $.each(data.points, function () {
        ret += '<br/>' + this.series.name + ': ';
        ret += Math.round(this.y * 100) / 100;
    });
    return ret;
}

function format_number_by_step(value, unit, step) {
    if (value > (step * step * step * step)) {
        value = value / (step * step * step * step);
        return Math.round(value * 100) / 100 + " T" + unit;
    } else if (value > (step * step * step)) {
        value = value / (step * step * step);
        return Math.round(value * 100) / 100 + " G" + unit;
    } else if (value > (step * step)) {
        value = value / (step * step);
        return Math.round(value * 100) / 100 + " M" + unit;
    } else if (value > (step)) {
        value = value / (step);
        return Math.round(value * 100) / 100 + " K" + unit;
    } else {
        return value + " " + unit;
    }
}

function render_connection_chart(data, elemid) {
    var xaxis_step = calculate_interval(data[0].length);
    var opts = {
        credits: {
            text: ''
        },
        chart: {zoomType: 'x'},
        colors: ['#367fa9', '#00a65a'],
        title: {text: "Connections"},
        yAxis: {title: {text: "connections"}, min: 0},
        xAxis: {
            type: "category",
            tickInterval: xaxis_step,
            startOnTick: true
        },
        series: [
            {
                name: "Connections/S",
                data: data[0]
            }
        ],
        legend: {
            layout: 'veritcal',
            align: 'right',
            verticalAlign: 'top',
            floating: true,
            borderWidth: 1
        },
        tooltip: {
            shared: true,
            crosshairs: true,
            formatter: function () {
                return tooltip_format_connection(this);
            }
        }
    };
    $(elemid).highcharts(opts);
}

function render_bandwidth_chart(data, elemid) {
    var xaxis_step = calculate_interval(data[0].length);
    var opts = {
        credits: {
            text: ''
        },
        chart: {zoomType: 'x'},
        colors: ['#00a65a', '#367fa9'],
        title: {text: "Bandwidth"},
        yAxis: {title: {text: "bps"}, min: 0},
        xAxis: {
            type: "category",
            tickInterval: xaxis_step,
            startOnTick: true
        },
        series: [
            {
                name: "Inbound",
                data: data[0]
            },
            {
                name: "Outbound",
                data: data[1]
            }
        ],
        legend: {
            layout: 'veritcal',
            align: 'right',
            verticalAlign: 'top',
            floating: true,
            borderWidth: 1
        },
        tooltip: {
            shared: true,
            crosshairs: true,
            formatter: function () {
                var axis_title = this.points[0].series.yAxis.axisTitle;
                if (axis_title) {
                    var title_text = axis_title.textStr;
                } else {
                    var title_text = "";
                }
                if (title_text == "bps") {
                    return tooltip_format_unit(this, "bps", 1000);
                } else if (title_text == "Bps") {
                    return tooltip_format_unit(this, "Bps", 1024);
                } else {
                    return tooltip_format_unit(this, "", 1000);
                }
            }
        }
    };
    $(elemid).highcharts(opts);
}

function show_customer_detail(elem) {
    var elem = $(elem);
    var emodal = $("#customer-detail-modal");
    emodal.unbind("shown.bs.modal");
    emodal.unbind("show.bs.modal");
    emodal.on("show.bs.modal", function() {
        render_customer_modal(elem);
    });
    emodal.on("shown.bs.modal", function() {
        render_customer_modal_chart(elem);
    });
    emodal.modal("show");
}

function show_customer_config(elem) {
    var elem = $(elem);
    var emodal = $("#customer-config-modal");
    emodal.unbind('show.bs.modal');
    emodal.on('show.bs.modal', function() {
        $.ajax({
            async: false,
            method: "GET",
            url: "/admin/customers/" + elem.data("id") + "/config",
            statusCode: {
                200: function(data) {
                    $("#customer-config-config").html(data['config']);
                }
            }
        })
    });
    emodal.modal("show");
}

function update_license(elem) {
    var elem = $(elem);
    var url = elem.attr("post-url");
    $("#license-modal").unbind("show.bs.modal");
    $("#license-modal").on("show.bs.modal", function() {
        $("#license-text").val("").focus();
    })
    $("#license-modal-submit").unbind("click")
    $("#license-modal-submit").click(function() {
        var license = $("#license-text").val();
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({"license": license}),
            statusCode: {
                200: function() {
                    window.location.reload(true);
                },
                400: function(data, text) {
                    alert(data.responseText);
                }
            }
        });
    });
    $("#license-modal").modal("show");
    return false;
}
