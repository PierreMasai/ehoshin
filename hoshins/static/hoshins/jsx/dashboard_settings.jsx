var app = app || {};

HoshinItemView = React.createClass({
    changeHoshin: function(event) {
        event.preventDefault();
        var data = this.props.model.attributes;

        renderHoshin(data);

        $("#teamDashboardTabs").find("li").removeClass('active');
        $(ReactDOM.findDOMNode(this)).addClass('active');
    },
    render: function() {
        var data = this.props.model.attributes;
        var active='';

        if(this.props.index == 1) {
            renderHoshin(data);
            active = 'active';
        }

        return (
            <li className={active}><a href="" onClick={this.changeHoshin} >{data.name}</a></li>
        );
    }
});

HoshinList = br.List.extend({
    ItemView: HoshinItemView,
    url: app.getUrlResource('hoshins'),
    render: function (Nodes) {
        return (
            <ul className="nav nav-pills nav-justified">
                { Nodes }
            </ul>
        );
    }
});

hoshinList = new HoshinList('teamDashboardTabs');
hoshinList.fetch();

Item = Backbone.Model.extend({
  urlRoot: app.getUrlResource('items')
});

Items = Backbone.Collection.extend({
    url: app.getUrlResource('items'),
    model: Item,
    all : function () {
        this.url = app.getUrlResource('items');
        return this;
    },
    query : function (query) {
        this.all();

        query = _.map(query, function(value, key){
            return key + "=" + value
        }).join("&");

      this.url = this.url+'?'+query;
      return this;
    }
});

var items = new Items();

Comment = Backbone.Model.extend({
  urlRoot: app.getUrlResource('comments')
});

Comments = Backbone.Collection.extend({
    url: app.getUrlResource('comments'),
    model: Item,
    all : function () {
        this.url = app.getUrlResource('comments');
        return this;
    },
    query : function (query) {
        this.all();

        query = _.map(query, function(value, key){
            return key + "=" + value
        }).join("&");

      this.url = this.url+'?'+query;
      return this;
    }
});

var comments = new Comments();

renderHoshin = function(hoshin) {
    items.query({parent:hoshin.id});
    items.fetch({
        success: function(result){
            var labels = _.map(result.models, function(model) { return model.attributes.name; });
            labels.unshift('Hoshin overall');

            var chart = renderGraph(labels);

            var models = result.models.slice(0);
            models.unshift({attributes: hoshin});

            _.map(models, function(model, index) {
                comments.query({parent: model.attributes.global_id})
                        .fetch({ success: function(result) {
                                    chart.data.datasets[0].data[index] = result.length;
                                    chart.update();
                                 }
                        });
            });
        }
    });
    renderIndicators(hoshin);

    $("#hoshinSynthesis").attr('href', ['', TEAM_NAME, 'api', 'hoshin_synthesis', hoshin.id].join('/'));
    $("#itemSynthesis").attr('href', ['', TEAM_NAME, 'api', 'leader_synthesis', hoshin.id + '?items=all'].join('/'));
};

renderIndicators = function(hoshin) {
    var values = {
        'Themes': hoshin.nb_items,
        'Concrete actions': hoshin.nb_implementation_priorities,
        'Comments': hoshin.nb_comments,
        'Users': hoshin.nb_users,
        'One comment': hoshin.nb_commentators,
        'Many comments': hoshin.nb_chatty_commentators
    };

    var container = $("#teamDashboardIndicators");
    container.empty();

    _.mapObject(values, function(val, key) {
      container.append('<div class="col-xs-6 col-sm-4 col-md-2">' +
          '<span>'+key+'</span>' +
          '<h3>'+val+'</h3>' +
          '</div>');
    });
};

initChart = function() {
    var ctx = $("#curve").get(0).getContext("2d");
    var data = {
        labels: [],
        datasets: [
            {
                label: "the number of comments per themes",
                fillColor: "rgba(220,220,220,0.5)",
                strokeColor: "rgba(220,220,220,0.8)",
                highlightFill: "rgba(220,220,220,0.75)",
                highlightStroke: "rgba(220,220,220,1)",
                data: []
            }
        ]
    };

    app.chart = new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
            scales: {
                yAxes: [{
                    display: true,
                    ticks: {
                        beginAtZero: true   // minimum value will be 0.
                    }
                }]
            },
            responsive: true,
            maintainAspectRatio: false,
        }
    });
};

initChart();

renderGraph = function(labels) {
    var values = Array.apply(null, Array(labels.length)).map(Number.prototype.valueOf,0);

    app.chart.clear();
    app.chart.data.labels = labels;
    app.chart.data.datasets[0].data = values;
    app.chart.update();

    return app.chart;
};