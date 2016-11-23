/**
 * AdminLTE Demo Menu
 * ------------------
 * You should not use this file in production.
 * This file is for demo purposes only.
 */
(function ($, AdminLTE) {

  "use strict";

  /**
   * List of all the available skins
   *
   * @type Array
   */
  var my_skins = [
    "skin-blue",
    "skin-black",
    "skin-red",
    "skin-yellow",
    "skin-purple",
    "skin-green",
    "skin-blue-light",
    "skin-black-light",
    "skin-red-light",
    "skin-yellow-light",
    "skin-purple-light",
    "skin-green-light"
  ];

  //Create the new tab
  var tab_pane = $("<div />", {
    "id": "control-sidebar-theme-demo-options-tab",
    "class": "tab-pane active"
  });

  //Create the tab button
  var tab_button = $("<li />", {"class": "active"})
      .html("<a href='#control-sidebar-theme-demo-options-tab' data-toggle='tab'>"
      + "<i class='fa fa-wrench'></i>"
      + "</a>");

  //Add the tab button to the right sidebar tabs
  $("[href='#control-sidebar-home-tab']")
      .parent()
      .before(tab_button);

  //Create the menu
  var demo_settings = $("<div />");

  //Layout options
  demo_settings.append(
      "<h4 class='control-sidebar-heading'>"
      + "Layout Options"
      + "</h4>"
        //Fixed layout
      + "<div class='form-group'>"
      + "<label class='control-sidebar-subheading'>"
      + "<input type='checkbox' data-layout='fixed' class='pull-right'/> "
      + "Fixed layout"
      + "</label>"
      + "<p>Activate the fixed layout. You can't use fixed and boxed layouts together</p>"
      + "</div>"
        //Boxed layout
      + "<div class='form-group'>"
      + "<label class='control-sidebar-subheading'>"
      + "<input type='checkbox' data-layout='layout-boxed'class='pull-right'/> "
      + "Boxed Layout"
      + "</label>"
      + "<p>Activate the boxed layout</p>"
      + "</div>"
        //Sidebar Toggle
      + "<div class='form-group'>"
      + "<label class='control-sidebar-subheading'>"
      + "<input type='checkbox' data-layout='sidebar-collapse' class='pull-right'/> "
      + "Toggle Sidebar"
      + "</label>"
      + "<p>Toggle the left sidebar's state (open or collapse)</p>"
      + "</div>"
        //Sidebar mini expand on hover toggle
      + "<div class='form-group'>"
      + "<label class='control-sidebar-subheading'>"
      + "<input type='checkbox' data-enable='expandOnHover' class='pull-right'/> "
      + "Sidebar Expand on Hover"
      + "</label>"
      + "<p>Let the sidebar mini expand on hover</p>"
      + "</div>"
        //Control Sidebar Toggle
      + "<div class='form-group'>"
      + "<label class='control-sidebar-subheading'>"
      + "<input type='checkbox' data-controlsidebar='control-sidebar-open' class='pull-right'/> "
      + "Toggle Right Sidebar Slide"
      + "</label>"
      + "<p>Toggle between slide over content and push content effects</p>"
      + "</div>"
        //Control Sidebar Skin Toggle
      + "<div class='form-group'>"
      + "<label class='control-sidebar-subheading'>"
      + "<input type='checkbox' data-sidebarskin='toggle' class='pull-right'/> "
      + "Toggle Right Sidebar Skin"
      + "</label>"
      + "<p>Toggle between dark and light skins for the right sidebar</p>"
      + "</div>"
  );
  var skins_list = $("<ul />", {"class": 'list-unstyled clearfix'});

  //Dark sidebar skins
  var skin_blue =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-blue' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px; background: #367fa9;'></span><span class='bg-light-blue' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #222d32;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin'>Blue</p>");
  skins_list.append(skin_blue);
  var skin_black =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-black' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div style='box-shadow: 0 0 2px rgba(0,0,0,0.1)' class='clearfix'><span style='display:block; width: 20%; float: left; height: 7px; background: #fefefe;'></span><span style='display:block; width: 80%; float: left; height: 7px; background: #fefefe;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #222;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin'>Black</p>");
  skins_list.append(skin_black);
  var skin_purple =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-purple' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px;' class='bg-purple-active'></span><span class='bg-purple' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #222d32;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin'>Purple</p>");
  skins_list.append(skin_purple);
  var skin_green =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-green' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px;' class='bg-green-active'></span><span class='bg-green' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #222d32;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin'>Green</p>");
  skins_list.append(skin_green);
  var skin_red =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-red' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px;' class='bg-red-active'></span><span class='bg-red' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #222d32;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin'>Red</p>");
  skins_list.append(skin_red);
  var skin_yellow =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-yellow' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px;' class='bg-yellow-active'></span><span class='bg-yellow' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #222d32;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin'>Yellow</p>");
  skins_list.append(skin_yellow);

  //Light sidebar skins
  var skin_blue_light =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-blue-light' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px; background: #367fa9;'></span><span class='bg-light-blue' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #f9fafc;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin' style='font-size: 12px'>Blue Light</p>");
  skins_list.append(skin_blue_light);
  var skin_black_light =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-black-light' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div style='box-shadow: 0 0 2px rgba(0,0,0,0.1)' class='clearfix'><span style='display:block; width: 20%; float: left; height: 7px; background: #fefefe;'></span><span style='display:block; width: 80%; float: left; height: 7px; background: #fefefe;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #f9fafc;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin' style='font-size: 12px'>Black Light</p>");
  skins_list.append(skin_black_light);
  var skin_purple_light =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-purple-light' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px;' class='bg-purple-active'></span><span class='bg-purple' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #f9fafc;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin' style='font-size: 12px'>Purple Light</p>");
  skins_list.append(skin_purple_light);
  var skin_green_light =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-green-light' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px;' class='bg-green-active'></span><span class='bg-green' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #f9fafc;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin' style='font-size: 12px'>Green Light</p>");
  skins_list.append(skin_green_light);
  var skin_red_light =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-red-light' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px;' class='bg-red-active'></span><span class='bg-red' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #f9fafc;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin' style='font-size: 12px'>Red Light</p>");
  skins_list.append(skin_red_light);
  var skin_yellow_light =
      $("<li />", {style: "float:left; width: 33.33333%; padding: 5px;"})
          .append("<a href='javascript:void(0);' data-skin='skin-yellow-light' style='display: block; box-shadow: 0 0 3px rgba(0,0,0,0.4)' class='clearfix full-opacity-hover'>"
          + "<div><span style='display:block; width: 20%; float: left; height: 7px;' class='bg-yellow-active'></span><span class='bg-yellow' style='display:block; width: 80%; float: left; height: 7px;'></span></div>"
          + "<div><span style='display:block; width: 20%; float: left; height: 20px; background: #f9fafc;'></span><span style='display:block; width: 80%; float: left; height: 20px; background: #f4f5f7;'></span></div>"
          + "</a>"
          + "<p class='text-center no-margin' style='font-size: 12px;'>Yellow Light</p>");
  skins_list.append(skin_yellow_light);

  demo_settings.append("<h4 class='control-sidebar-heading'>Skins</h4>");
  demo_settings.append(skins_list);

  tab_pane.append(demo_settings);
  $("#control-sidebar-home-tab").after(tab_pane);

  setup();

  /**
   * Toggles layout classes
   *
   * @param String cls the layout class to toggle
   * @returns void
   */
  function change_layout(cls) {
    $("body").toggleClass(cls);
    AdminLTE.layout.fixSidebar();
    //Fix the problem with right sidebar and layout boxed
    if (cls == "layout-boxed")
      AdminLTE.controlSidebar._fix($(".control-sidebar-bg"));
    if ($('body').hasClass('fixed') && cls == 'fixed') {
      AdminLTE.pushMenu.expandOnHover();
      AdminLTE.layout.activate();
    }
    AdminLTE.controlSidebar._fix($(".control-sidebar-bg"));
    AdminLTE.controlSidebar._fix($(".control-sidebar"));
  }

  /**
   * Replaces the old skin with the new skin
   * @param String cls the new skin class
   * @returns Boolean false to prevent link's default action
   */
  function change_skin(cls) {
    $.each(my_skins, function (i) {
      $("body").removeClass(my_skins[i]);
    });

    $("body").addClass(cls);
    store('skin', cls);
    return false;
  }

  /**
   * Store a new settings in the browser
   *
   * @param String name Name of the setting
   * @param String val Value of the setting
   * @returns void
   */
  function store(name, val) {
    if (typeof (Storage) !== "undefined") {
      localStorage.setItem(name, val);
    } else {
      window.alert('Please use a modern browser to properly view this template!');
    }
  }

  /**
   * Get a prestored setting
   *
   * @param String name Name of of the setting
   * @returns String The value of the setting | null
   */
  function get(name) {
    if (typeof (Storage) !== "undefined") {
      return localStorage.getItem(name);
    } else {
      window.alert('Please use a modern browser to properly view this template!');
    }
  }

  /**
   * Retrieve default settings and apply them to the template
   *
   * @returns void
   */
  function setup() {
    var tmp = get('skin');
    if (tmp && $.inArray(tmp, my_skins))
      change_skin(tmp);

    //Add the change skin listener
    $("[data-skin]").on('click', function (e) {
      if($(this).hasClass('knob'))
        return;
      e.preventDefault();
      change_skin($(this).data('skin'));
    });

    //Add the layout manager
    $("[data-layout]").on('click', function () {
      change_layout($(this).data('layout'));
    });

    $("[data-controlsidebar]").on('click', function () {
      change_layout($(this).data('controlsidebar'));
      var slide = !AdminLTE.options.controlSidebarOptions.slide;
      AdminLTE.options.controlSidebarOptions.slide = slide;
      if (!slide)
        $('.control-sidebar').removeClass('control-sidebar-open');
    });

    $("[data-sidebarskin='toggle']").on('click', function () {
      var sidebar = $(".control-sidebar");
      if (sidebar.hasClass("control-sidebar-dark")) {
        sidebar.removeClass("control-sidebar-dark")
        sidebar.addClass("control-sidebar-light")
      } else {
        sidebar.removeClass("control-sidebar-light")
        sidebar.addClass("control-sidebar-dark")
      }
    });

    $("[data-enable='expandOnHover']").on('click', function () {
      $(this).attr('disabled', true);
      AdminLTE.pushMenu.expandOnHover();
      if (!$('body').hasClass('sidebar-collapse'))
        $("[data-layout='sidebar-collapse']").click();
    });

    // Reset options
    if ($('body').hasClass('fixed')) {
      $("[data-layout='fixed']").attr('checked', 'checked');
    }
    if ($('body').hasClass('layout-boxed')) {
      $("[data-layout='layout-boxed']").attr('checked', 'checked');
    }
    if ($('body').hasClass('sidebar-collapse')) {
      $("[data-layout='sidebar-collapse']").attr('checked', 'checked');
    }

  }
})(jQuery, $.AdminLTE);

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
        var nelem = $("#create-customer-name");
        nelem.val("").focus();
    });
    $("#create-customer-submit").unbind("click");
    $("#create-customer-submit").click(function() {
        var name = $("#create-customer-name").val();
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'name': name}),
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
        $("#server-hostname").focus();
    });
    $("#server-modal-submit").unbind("click");
    $("#server-modal-submit").click(function() {
        var hostname = $("#server-hostname").val();
        var ip = $("#server-ip").val();
        var comments = $("#server-comments").val();
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'hostname': hostname, 'ip': ip, 'comments': comments}),
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
        $.ajax({
            async: false,
            type: "POST",
            url: url,
            data: add_csrf_token({'hostname': hostname, 'ip': ip, 'comments': comments}),
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
    emodal.on("shown.bs.modal", function() {
        render_customer_modal(elem);
    });
    emodal.modal("show");
}
