function get_csrf_token() {
    return $("input[name='csrfmiddlewaretoken']").val();
}

function add_csrf_token(data) {
    data["csrfmiddlewaretoken"] = get_csrf_token();
    return data;
}

function double_check() {
    if(confirm("Are you sure?")) {
        return true;
    }
    return false;
}

function create_customer(elem) {
    var elem = $(elem);
    var url = elem.attr("post-url");
    $("#create-customer-modal").unbind("show.bs.modal");
    $("#create-customer-modal").on("show.bs.modal", function() {
        $("#create-customer-name").val("").focus();
        $("#create-customer-servers").val(1);
    });
    $("#create-customer-submit").unbind("click");
    $("#create-customer-submit").click(function() {
        var name = $("#create-customer-name").val();
        var servers = $("#create-customer-servers").val();
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'name': name, 'servers': servers}),
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

function render_error(data, prefix) {
    for(k in data.responseJSON) {
        var value = data.responseJSON[k];
        var ielem = $(prefix + "" + k);
        ielem.parent().parent().addClass("has-error");
    }
}

function create_server(elem) {
    var elem = $(elem);
    var url = elem.attr("post-url");
    var emodal = $("#server-modal");
    $("#server-modal-title").html("Create Server");
    emodal.unbind("show.bs.modal");
    emodal.unbind("shown.bs.modal");
    emodal.on("show.bs.modal", function() {
        var elem_list = ["#server-hostname", "#server-ip", "#server-comments"]
        for(eid in elem_list) {
            var ielem = $(elem_list[eid]);
            ielem.val("")
            ielem.parent().parent().removeClass("has-error");
        }
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
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'hostname': hostname, 'ip': ip, 'comments': comments, 'encryption': encryption, 'status': status}),
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
    $("#server-modal-title").html("Edit Server");
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
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'hostname': hostname, 'ip': ip, 'comments': comments, 'encryption': encryption, 'status': status}),
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
    $(pfx+"userid").html(elem.data("userid"));
    $(pfx+"userid-2").html(elem.data("userid"));
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
                for (var i in data['servers']) {
                    var item = data['servers'][i];
                    servers_html += '<div><span style="min-width:100px;padding-right:5px;">Encryption: ' + item[2].toUpperCase() + '</span><span>IP: ' + item[1] + "</span></div>";
                }
                $(pfx+"servers").html(servers_html);
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
                render_chart(data, pfx+"bandwidth-chart");
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

function render_chart(data, elemid) {
    var xaxis_step = calculate_interval(data[0].length);
    var opts = {
        credits: {
            text: ''
        },
        chart: {zoomType: 'x'},
        colors: ['#337ab7', '#4cae4c'],
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
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 30,
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
