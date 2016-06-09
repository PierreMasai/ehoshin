var app = app || {};

links = {
    get_url: function() {
        var url = this.props.data.url.slice();
        if(this.props.hasOwnProperty('model'))
            url.push(this.props.model.id);

        if(url.length > 5)
            url = url.slice(0,5);

        return url;
    },
    go: function(event, urlSplitted) {
        event.preventDefault();
        var url = urlSplitted.join('/');

        var currentUrl = Backbone.history.getFragment();
        if(currentUrl !== url)
            app.router.navigate(url, {trigger:true});
    },
    parent: function(event) {
        var url = this.get_url().slice(0,-1);
        this.go(event, url);
    },
    myself: function(event) {
        var url = this.get_url();

        if(url.length == 5)
            this.comments(event);
        else
            this.go(event, url);
    },
    comments: function(event) {
        var url = this.get_url().slice();
        url.push('comments');

        this.go(event, url);
    }
};

function replaceAll(str, find, replace) {
  return str.replace(new RegExp(find, 'g'), replace);
}

Link = React.createClass({
    render: function() {
        return(
            <span className="label label-default link" style={{backgroundColor: this.props.color}}>
                {this.props.name} {this.props.index}
            </span>
        );
    }
});

ItemBottom = React.createClass({
    render: function() {
        var data = this.props.model;

        var target = replaceAll(data.target, '\n', '<br />');

        var index = 0;
        var Links = data.references.map(function(link) {
            index +=1;
            link['key'] = index;
            return React.createElement(Link, link);
        });

        if(index == 0)
            Links = <span className="link no-link">none</span>;

        return(
            <table>
                <tbody>
                    <tr>
                        <td>Target</td>
                        <td><span dangerouslySetInnerHTML={ {__html:target} } /></td>
                    </tr>
                    <tr>
                        <td>Leader</td>
                        <td>{data.leader}</td>
                    </tr>
                    <tr>
                        <td>References</td>
                        <td>{Links}</td>
                    </tr>
                </tbody>
            </table>
        );
    }
});


ItemView = React.createClass({
    mixins: [{delete: BreakLine.formHelper.delete}, links],
    render: function() {
        var data = this.props.model.attributes;
        var managePart = "";
        var size = "col-sm-12";

        if(USER.isModerator) {
            managePart = <app.aToogler model={this.props.model} classe_names="col-sm-1" right={true} deleteHandler={this.delete}/>;
            size = "col-sm-11";
        }

        var className = "row panel panel-default";
        if(this.props.model._isOptimistic)
            className += " isOptimistic";

        return (
            <div className={className}>
                <div className="col-sm-12 panel-heading item_box">
                    <div className={size}>
                        <a href="" onClick={this.myself}>
                            <h3 data-toggle="tooltip" data-placement="top" title="Click to have more information">
                                {this.props.index}. {data.name}
                            </h3>
                        </a>
                        < ItemBottom model={data} />
                    </div>
                    {managePart}
                </div>
            </div>
        );
      }
});


PriorityView = React.createClass({
    mixins: [{delete: BreakLine.formHelper.delete}, links],
    render: function() {
        var data = this.props.model.attributes;
        var managePart = "";
        var size = "col-sm-12";

        if(USER.isModerator) {
            managePart = <app.aToogler model={this.props.model} classe_names="col-sm-1" right={true} deleteHandler={this.delete}/>;
            size = "col-sm-11";
        }

        var className = "row panel panel-default";
        if(this.props.model._isOptimistic)
            className += " isOptimistic";

        return (
            <div className={className}>
                <div className="col-sm-12 panel-heading item_box">
                    <div className={size}>
                        <a href="" onClick={this.myself}>
                            <table>
                                <tbody>
                                    <tr>
                                        <td>{this.props.index}.</td>
                                        <td>{data.target}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </a>
                    </div>
                    {managePart}
                </div>
            </div>
        );
      }
});

Toggle = React.createClass({
    componentDidMount: function() {
        var DOMNode = ReactDOM.findDOMNode(this);
        var parent = this;

        var inputs = $(DOMNode).find('input');
        var index = $(inputs[1]);
        var name = $($(DOMNode).find('td:first')).text();

        $(inputs[0]).change(function() {
            if($(this).prop('checked')) {
                parent.props.toggle_link(name, true, index.val());
                index.show();
            }
            else {
                parent.props.toggle_link(name, false);
                index.hide();
            }
        }).bootstrapToggle();

        index.change(function() {
            parent.props.toggle_link(name, true, index.val());
        })
    },
    render: function() {

        var className = "form-control";
        if(!this.props.checked)
            className += ' soft-hidden';

        return (
            <tr>
                <td>{ this.props.name }</td>
                <td>
                    <input defaultChecked={ this.props.checked } type="checkbox" data-toggle="toggle" />
                </td>
                <td>
                    <input type="text" className={className} defaultValue={this.props.text} placeholder="Index (eg: 1.5)"/>
                </td>
            </tr>
        );
    }
});

function cleanArray(actual) {
  var newArray = new Array();
  for (var i = 0; i < actual.length; i++) {
    if (actual[i]) {
      newArray.push(actual[i]);
    }
  }
  return newArray;
}

ItemFormView = React.createClass({
    mixins: [_.omit(BreakLine.formHelper,'getInitialState')],
    fields: {
        "target": "Target",
        "name": "Name",
        "leader": "Leader",
    },
    is_in: function(name, index) {
        var data = this.state.model.attributes;
        return _.reduce(data.references, function(is_in, link){
                if(link.name == name) {
                    link.index = index;
                    return true;
                }
                else
                    return is_in;
            }, false);
    },
    getReference: function(name) {
        var data = this.state.model.attributes;
        return _.reduce(data.references, function(ref, link){
                if(link.name == name) {
                    return link;
                }
                else
                    return ref;
            }, null);
    },
    toggle_link: function(name, checked, index){
        var data = this.props.model.attributes;
        if(!checked) {
            var links = _.map(data.references, function(link) {
                if(link.name != name)
                    return link;
            });
            data.references = cleanArray(links);
        }
        else {
            var isIn = this.is_in(name, index);

            if(!isIn) {
                var link = _.reduce(app.referenceList, function(elt, link){
                    if(link.name == name) {
                        return {
                            'name': link.name,
                            'color': link.color,
                            'index': index
                        };
                    }
                    else
                        return elt;
                }, null);

                if(link)
                    data.references.push(link);
            }
        }
    },
    verify: function() {
        var errors = {};
        var data = this.state.model.attributes;

        if(_.isUndefined(data.name) || data.name === "")
            errors['name'] = ['This field must not be blank'];

        if(_.isUndefined(data.target) || data.target === "")
            errors['target'] = ['This field must not be blank'];

        if(_.isUndefined(data.leader) || data.leader === "")
            errors['leader'] = ['This field must not be blank'];

        return errors;
    },
    getInitialState: function() {
        return {model: this.props.model};
    },
    save: function(event) {
        event.preventDefault();

        if(this.state.model.isNew()) {
            var url = this.props.data.url;
            var parent = url[url.length-1];
            this.state.model.attributes.parent = parseInt(parent);
        }

        this.saveModel();
    },
    componentDidMount: function() {
        var DOMNode = ReactDOM.findDOMNode(this);
        var substringMatcher = function(strs) {
          return function findMatches(q, cb) {
            var matches, substringRegex;

            // an array that will be populated with substring matches
            matches = [];

            // regex used to determine if a string contains the substring `q`
            substrRegex = new RegExp(q, 'i');

            // iterate through the pool of strings and for any string that
            // contains the substring `q`, add it to the `matches` array
            $.each(strs, function(i, str) {
              if (substrRegex.test(str)) {
                matches.push(str);
              }
            });

            cb(matches);
          };
        };

        var names = _.map(app.userList.model.models, function(model){
            var d = model.attributes;
            return d.first_name + " " + d.last_name
        });

        var parent = this;
        $($(DOMNode).find(".typeahead")).typeahead({
          hint: true,
          highlight: true,
          minLength: 1
        },
        {
          name: 'names',
          source: substringMatcher(names)
        }).bind('typeahead:change', function(ev, val) {
            parent.state.model.attributes['leader'] = val;
            parent.replaceState(parent.state);
        });

    },
    render: function() {
        var data = this.state.model.attributes;
        var parent= this;
        var header = "Create a new " + this.props.type;
        if(!this.state.model.isNew())
            header = "Modify it!";

        var index = 0;
        var Links = _.map(app.referenceList, function(reference) {
            var link = parent.getReference(reference.name);
            var checked = !_.isNull(link);
            var text = checked ? link.index : '';

            index += 1;
            return <Toggle key={index}
                           name={reference.name}
                           text={text}
                           checked={checked}
                           toggle_link={parent.toggle_link}/>
        });

        return (
          <div className="panel panel-default">
              <div className="panel-heading">
                  <div className="row">
                      <h3>
                          {header}
                      </h3>
                  </div>
                  <BreakLine.Errors errors={this.state.model._errors} />
                  <div className="row form-group">
                    <label htmlFor="name">Name</label>
                    <input type="text" className="form-control" data-model="name" value={data.name} onChange={this.valueHandleChange}/>
                  </div>

                  <div className="row form-group">
                    <label htmlFor="leader">Leader</label>
                    <input type="text" data-model="leader" className="form-control typeahead" value={data.leader} onChange={this.valueHandleChange}/>
                  </div>

                  <div className="row form-group">
                    <label htmlFor="target">Target</label>
                    <textarea type="text" className="form-control"
                              data-model="target" value={data.target}
                              onChange={this.valueHandleChange}
                              rows="4" />
                  </div>
                  <div className="row">
                      <label htmlFor="target">Links:</label>
                      <table>
                          <tbody>
                            {Links}
                          </tbody>
                      </table>
                  </div>
                    <div className="row">
                        <div className="col-xs-4 col-xs-offset-4">
                            <button type="button" className="btn flat btn-default" onClick={this.save}>Save</button>
                        </div>
                    </div>
              </div>
          </div>
        );
      }
});


function clone(obj) {
    var copy;

    // Handle the 3 simple types, and null or undefined
    if (null == obj || "object" != typeof obj) return obj;

    // Handle Date
    if (obj instanceof Date) {
        copy = new Date();
        copy.setTime(obj.getTime());
        return copy;
    }

    // Handle Array
    if (obj instanceof Array) {
        copy = [];
        for (var i = 0, len = obj.length; i < len; i++) {
            copy[i] = clone(obj[i]);
        }
        return copy;
    }

    // Handle Object
    if (obj instanceof Object) {
        copy = {};
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
        }
        return copy;
    }

    throw new Error("Unable to copy obj! Its type isn't supported.");
}

PriorityFormView = React.createClass({
    mixins: [_.omit(BreakLine.formHelper,'getInitialState')],
    fields: {
        "target": "Title"
    },
    verify: function() {
        var errors = {};
        var data = this.state.model.attributes;

        if(_.isUndefined(data.target) || data.target === "")
            errors['target'] = ['This field must not be blank'];

        return errors;
    },
    getInitialState: function() {
        return {model: this.props.model};
    },
    save: function(event) {
        event.preventDefault();

        if(this.state.model.isNew()) {
            var url = this.props.data.url;
            var parent = url[url.length-1];
            this.state.model.attributes.parent = parseInt(parent);
        }

        this.saveModel();
    },
    render: function() {
        var data = this.state.model.attributes;
        var parent= this;
        var header = "Create a new " + this.props.type;
        if(!this.state.model.isNew())
            header = "Modify it!";


        return (
          <div className="panel panel-default">
              <div className="panel-heading">
                  <div className="row">
                      <h3>
                          {header}
                      </h3>
                  </div>
                  <BreakLine.Errors errors={this.state.model._errors} />

                  <div className="row form-group">
                    <label htmlFor="target">Title</label>
                    <textarea type="text" className="form-control"
                              data-model="target" value={data.target}
                              onChange={this.valueHandleChange}
                              rows="4" />
                  </div>
                    <div className="row">
                        <div className="col-xs-4 col-xs-offset-4">
                            <button type="button" className="btn flat btn-default" onClick={this.save}>Save</button>
                        </div>
                    </div>
              </div>
          </div>
        );
      }
});

Help = React.createClass({
    componentDidMount: function() {
        var DOMNode = $(ReactDOM.findDOMNode(this));

        DOMNode.find('a').click(function(event) {
            event.preventDefault();
            var help = app.helpList.model.findWhere({type:'participation'});
            if(!_.isUndefined(help))
                help.destroy();

            DOMNode.hide();
        });
    },
    render: function() {
        return (
            <div className="bs-callout bs-callout-danger">
                <a className="right" href="" data-toggle="tooltip" data-placement="left"
                   title="Don't show this message anymore">
                    <span className="glyphicon glyphicon-remove" />
                </a>

                <h4>You’re welcome to give your feedback on</h4>
                <p>
                    a) The Hoshin overall by using the button on top right ‘Give your comments on the Hoshin overall’<br />
                    b) The hoshin themes, by clicking on the hoshin theme and using the button on top right ‘Give your comments on the theme’
                </p>
            </div>
        );
    }
});

app.ItemList = br.List.extend({
    ItemView: ItemView,
    FormView: ItemFormView,
    url: app.getUrlResource('items'),
    defaults: {
        owner:  USER,
        target: '',
        references: []
    },
    render: function (Nodes, modelForm) {
        var formPart = "";

        if(USER.isModerator)
            formPart = <this.FormView model={modelForm} data={this.data} type="theme"/>;

        if(Nodes.length == 0)
            Nodes = <h3 className="bg_text">There is no theme yet.</h3>;

        var help = "";
        if(app.helpList.model.where({type:'participation'}).length > 0)
            help = <Help />;

        return (
            <div>
                {help}
                {Nodes}
                {formPart}
            </div>
        );
    }
});

app.PriorityList = br.List.extend({
    ItemView: PriorityView,
    FormView: PriorityFormView,
    url: app.getUrlResource('implementation_priorities'),
    defaults: {
        owner:  USER,
        target: '',
        name: '/',
        leader: '/',
        references: []
    },
    render: function (Nodes, modelForm) {
        var formPart = "";

        if(USER.isModerator)
            formPart = <this.FormView model={modelForm} data={this.data} type="concrete action"/>;

        if(Nodes.length == 0)
            Nodes = <h3 className="bg_text">There is no concrete action yet.</h3>;

        return (
            <div>
                {Nodes}
                {formPart}
            </div>
        );
    }
});