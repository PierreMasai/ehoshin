var app = app || {};

/*
    redoPath: function(url) {
        var len = url.length;
        if(url[url.length-1] === "")
            len -= 1;

        var path_user = $($.find("#path_user")[0]);
        var pathSplitted = Array.apply(null, Array(len)).map(function () {});

        if(url[url.length-1] === "comments") {
            len -= 1;
            pathSplitted[len] = url[len];
        }



        app.hoshinList.doneFetching(function() {
          var data = app.hoshinList.get(url[0]);

            if(data)
                pathSplitted[0] = data.attributes.name;
        });

        // TODO: loop generalization (bug with i, always the last one)
        app.itemList.doneFetching(function() {
              var data = app.itemList.get(url[1]);
              if(data)
                  pathSplitted[1] = data.attributes.name;
              else
                  pathSplitted[1] = "";
            });

        var id = setInterval(isDone, 100);

          function isDone() {
              var done = true;
              pathSplitted.map(function(elt) {
                  if(typeof elt === "undefined")
                    done = false
              });
            //console.log(pathSplitted)
            if(done) {
                path_user.empty();
                pathSplitted = pathSplitted.map(function(elt) {
                    return "<span>" + elt + "</span>";
                });

                path_user.append(pathSplitted.join('<span class="glyphicon glyphicon-menu-right"></span>'));
                clearInterval(id);
            }
          }
    }
});
*/

HoshinHeaderView = React.createClass({
    mixins: [links],
    render: function() {
        return( <div className="row header_links">
            <a className="col-sm-offset-4 col-sm-4 text-center" onClick={this.myself} href=""><h4>Themes</h4></a>
            <a className="col-sm-4 text-right" onClick={this.comments} href="">
                <h4 className="important" >Give your comments on the Hoshin overall</h4>
            </a>
        </div> );
    }
});

ItemHeaderView = React.createClass({
    mixins: [links],
    render: function() {
        return(
            <div>
                <ItemBottom model={this.props.data.model.attributes} />
                <div className="row header_links">
                    <a className="col-sm-4 text-left" onClick={this.parent} href=""><h4>Go back to the Hoshin</h4></a>
                    <a className="col-sm-4 text-center" onClick={this.myself} href=""><h4>Concrete actions</h4></a>
                    <a className="col-sm-4 text-right" onClick={this.comments} href="">
                        <h4 className="important" >Give your comments on the theme</h4>
                    </a>
                </div>
            </div>
        );
    }
});

PriorityHeaderView = React.createClass({
    mixins: [links],
    render: function() {
        return(
            <div>
                <ItemBottom model={this.props.data.model.attributes} />
                <div className="row header_links">
                    <a className="col-sm-4 text-left" onClick={this.parent} href=""><h4>Go back to the Theme</h4></a>
                    <a className="col-sm-offset-4 col-sm-4 text-right" onClick={this.comments} href="">
                        <h4 className="important" >Give your comments on the concrete action</h4>
                    </a>
                </div>
            </div>
        );
    }
});

app.GlobalHeaderView = React.createClass({
    mixins: [links],
    render: function() {
        var data = this.props.model.attributes;

        var types_objects = {
            'Hoshin': <HoshinHeaderView data={
                {
                    url:this.props.url
                }
            }/>,
            'Theme': <ItemHeaderView data={
                {
                    url:this.props.url,
                    model:this.props.model
                }
            }/>,
            'Concrete action': <PriorityHeaderView data={
                {
                    url:this.props.url,
                    model:this.props.model
                }
            }/>
        };

        return (
            <div className="col-sm-12">
                <h3 className="col-sm-12">
                    {this.props.type} : {data.name}
                </h3>
                {types_objects[this.props.type]}
            </div>
        );
      }
});


app.RoutesManager = Backbone.Router.extend({
    routes: {
      ":name":       "redirectHoshin",
      ":name/":      "redirectHoshin",
      ":name/*path": "displayHoshin"

    },
    history: [],
    previousUrl: function() {
        return this.history[this.history.length-2];
    },
    updateHeaderItem: function(object_type, urlSplitted) {
        var global_id = _.last(urlSplitted);

        $.get(app.getUrlResource(object_type) + '/' + global_id)
            .done(function( attributes ) {
                var types_objects = {
                    'hoshins': 'Hoshin',
                    'items': 'Theme',
                    'implementation_priorities': 'Concrete action'
                };

                var params = {
                    model: {attributes: attributes},
                    url: urlSplitted,
                    type: types_objects[object_type]
                };

                ReactDOM.render(
                    React.createElement(app.GlobalHeaderView, params),
                                        document.getElementById("header_item")
                );
            });
    },
    setLoading: function(isLoading) {
        if(isLoading) {
            $("#commentList").addClass("isLoading");
            $("#itemList").addClass("isLoading");
        }
        else {
            $("#commentList").removeClass("isLoading");
            $("#itemList").removeClass("isLoading");
            window.scroll(0, 0);
        }
    },
    displayHoshin: function(name, path) {
        var parent = this;
        var pathSplitted = ['', name].concat(path.split("/"));
        var comments = false;

        var types_objects = {
            '3': 'hoshins',
            '4': 'items',
            '5': 'implementation_priorities'
        };

        if(_.last(pathSplitted) === "")
            pathSplitted.pop();

        this.history.push(pathSplitted);

        if(_.last(pathSplitted) === "comments") {
            pathSplitted.pop();
            comments = true;
        }

        if(isNaN(_.last(pathSplitted)))
            throw 'The url is wrong...';

        var object_type = types_objects[pathSplitted.length];
        this.setLoading(true);
        var global_id = _.last(pathSplitted);
        var idHoshin = pathSplitted[2];
        this.refreshIndicators(object_type, idHoshin);
        this.updateHeaderItem(object_type, pathSplitted);

        $(".hoshins_box").css("visibility", 'visible');
        $("#hoshinInformation").show();
        $("#header_item").show();

        var excelExport = $("#excelExport");
        if(object_type === 'hoshins' || excelExport.attr("href") == '') {
            excelExport.attr("href",
                app.getUrlResource('hoshins') + '/' + idHoshin +'?type=application/excel')
        }

        if(comments) {
            app.commentList.data = {
                url: pathSplitted
            };
            app.commentList.query({"parent": global_id, "type": object_type});
            app.commentList.fetch();
            app.commentList.doneFetching(function() {
                switchSection('commentList');
                parent.setLoading(false);
            });
        }
        else if(object_type === 'hoshins') {
            $("#leaderSynthesis").attr('href', ['', TEAM_NAME, 'api', 'leader_synthesis', global_id].join('/'));
            app.itemList.data = {
                url: pathSplitted
            };
            app.itemList.query({"parent": global_id});
            app.itemList.fetch();
            app.itemList.doneFetching(function() {
                switchSection('itemList');
                parent.setLoading(false);
            });
        }
        else {
            app.priorityList.data = {
                url: pathSplitted
            };
            app.priorityList.query({"parent": global_id});
            app.priorityList.fetch();
            app.priorityList.doneFetching(function() {
                var lastUrl = parent.previousUrl();

                if(app.priorityList.model.length == 0 && !(
                        !_.isUndefined(lastUrl) &&
                        _.last(lastUrl) == global_id && lastUrl.length == 4
                    )) {
                    var redirctionUrl = Backbone.history.getFragment() + '/comments';
                    app.router.navigate(redirctionUrl, {trigger:true});
                }
                else {
                    switchSection('priorityList');
                    parent.setLoading(false);
                }
            });
        }
    },
    /*
     * This function show the first hoshin when any is given
     * i.e, when someone try to reach the /home url, he will be
     * redirected to /home/first_hoshin_id (e.g /home/1)
     */
    redirectHoshin: function(name) {
        var parent = this;
        app.hoshinList.model.sort();
        var firstHoshin = _.first(app.hoshinList.model.models);

        if(_.isUndefined(firstHoshin)) {
            $("#hoshinInformation").hide();
            $("#header_item").hide();
            switchSection('noHoshinText');

            if (USER.isOwner || USER.isModerator) {
                $(".hoshins_box").css("visibility", 'visible');
                switchSection('noHoshinTextMo');
            }
            else
                switchSection('noHoshinTextNo');
        }
        else {
            var url = ['', name, firstHoshin.attributes.id];
            parent.navigate(url.join('/'), {trigger:true});
        }

    },
    resetIndicators: function() {
        var url = Backbone.history.getFragment().split('/');

        if(url.length >= 2) {
            var global_id = url[1];
            var object_type = 'hoshins';

            app.hoshinList.fetch();
            this.refreshIndicators(object_type, global_id);
        }
    },
    /*
     * If the size is one or if there is no indicators at the moment,
     * the new ones are fetch
     */
    refreshIndicators: function(object_type, idHoshin) {
        var indicatorBox = $("#hoshinIndicators");
        var isEmpty = !$.trim(indicatorBox.html());

        if(object_type === 'hoshins' || isEmpty) {
            app.hoshinList.doneFetching(function() {
                var model = app.hoshinList.model.findWhere({'id':parseInt(idHoshin)});
                if(model) {
                    $('.hoshin_name').text(model.attributes.name);
                    ReactDOM.render(
                        React.createElement(app.HoshinIndicatorList, model.attributes),
                        document.getElementById("hoshinIndicators")
                    );
                }
            });
        }
    }
});


function switchSection(sectionName) {
    var sections = ['noHoshinTextMo', 'noHoshinTextNo', 'itemList', 'priorityList', 'commentList'];

    $.each(sections, function(index, name) {
        if(name === sectionName)
            $('#' + name).show();
        else
            $('#' + name).hide();
    });
}

function showTeamSpace() {
    // Get the model of the current user and his follows
    app.userList = new app.UserList();
    app.helpList = new app.HelpList();

    switchSection('any');

    app.me = app.userList.get(USER.id);

    app.me.fetch().done(function(model) {
        app.helpList.fetch();

        app.helpList.doneFetching(function() {
            app.notifications.fetch();

            app.hoshinList = new app.HoshinList('hoshins_list');
            app.hoshinList.fetch();

            app.userList.query({team: TEAM_NAME});
            app.userList.fetch();
            app.userList.doneFetching(function() {
                app.itemList = new app.ItemList('itemList');
                app.priorityList = new app.PriorityList('priorityList');
                app.commentList = new app.CommentList('commentList');

                app.hoshinList.doneFetching(function() {
                    if(app.hoshinList.model.size() == 0) {
                        if (USER.isOwner || USER.isModerator) {
                            $(".hoshins_box").css("visibility", 'visible');
                            switchSection('noHoshinTextMo');
                        }
                        else
                            switchSection('noHoshinTextNo');
                    }
                    else {
                        $(".hoshins_box").css("visibility", 'visible');
                        $("#hoshinInformation").show();
                    }

                    app.router = new app.RoutesManager();
                    Backbone.history.start({pushState: true});
                });
            })
        });
    });
}


$(function (){
    function rgb2hex(rgb) {
        if (/^#[0-9A-F]{6}$/i.test(rgb)) return rgb;

        rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
        function hex(x) {
            return ("0" + parseInt(x).toString(16)).slice(-2);
        }
        return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
    }

    app.referenceList = _.map($('#referenceList').children().find('button'), function(reference) {
        var spans = $(reference).find('span');
        var color = $(spans[0]).css('background-color');

        return {
            'name': $(spans[1]).text(),
            'color': rgb2hex(color)
        };
    });

    if(!_.isUndefined(TEAM_NAME))
        showTeamSpace();
    else
        console.error("Any team name given in the url... How did you get there?")
});

