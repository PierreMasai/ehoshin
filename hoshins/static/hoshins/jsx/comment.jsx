var app = app || {};

String.prototype.replaceAll = function(search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

var getTypeFromPath = function() {
    var url = Backbone.history.location.pathname;
    var len = url.split('/').length;
    var result;

    switch(len) {
        case 4:
            result = 'hoshins';
            break;
        case 5:
            result = 'items';
            break;
        case 6:
            result = 'concrete_actions';
            break;
        default:
            result = 'any';
    }

    return result;
};


app.CommentHeader = React.createClass({
    render: function() {
        return (
            <span>
                { this.props.textBegin }
                <span style={{color: this.props.color}}>
                    { this.props.textColored }
                </span>
            </span>
        );
      }
});

app.CommentView = React.createClass({
    getType: function(action) {
        var type = getTypeFromPath();

        var results = {
            'hoshins': {
                'AD': 'theme'
            },
            'items': {
                'AD': 'concrete action',
                'MO': 'target\'s theme',
                //'RE': 'item'
            },
            'concrete_actions': {
                //'MO': 'concrete action',
                //'RE': 'concrete action'
            }
        };

        var result = results[type][action];
        if(action === 'MO')
            return result + " modification ";
        else if(action === 'AD')
            return result + ' addition ';
        else if(action === 'RE')
            return result + ' removal ';

        return ''
    },
    render: function() {
        var data = this.props.model.attributes;
        var managePart = "";
        var size = "col-sm-12";

        var owner_comment = false;
        if(data.owner) {
            if(USER.id == data.owner.id)
                owner_comment = true;
        }
        else if(USER.first_name + ' ' + USER.last_name == data.owner_temp)
            owner_comment = true;

        if(USER.isModerator || owner_comment) {
            managePart = <app.aToogler model={this.props.model} classe_names="col-sm-1" right={true}/>;
            size = "col-sm-11";
        }

        var messageType = "";

        if(data.type == "MO")
            messageType = <app.CommentHeader color="#805B15" textBegin="proposed the " textColored={this.getType(data.type)} />;
        else if(data.type == "AD")
            messageType = <app.CommentHeader color="#0D4D4B" textBegin="proposed a " textColored={this.getType(data.type)} />;
        else if(data.type == "RE")
            messageType = <app.CommentHeader color="#7E1518" textBegin="proposed the " textColored={this.getType(data.type)} />;

        var className = "row panel panel-default";
        if(this.props.model._isOptimistic)
            className += " isOptimistic";

        var author = data.owner_temp;
        if(data.owner_temp == "" && data.owner)
            author = data.owner.first_name + " " + data.owner.last_name;

        data.text = data.text.replaceAll('\n', '<br />');

        return (
          <div className={className}>
            <div className="col-sm-12 panel-heading">
                <div className={size}>
                    <strong>{author}</strong> { messageType }<br />
                    <p dangerouslySetInnerHTML={{__html: data.text}}></p>
                    <span className="date">{ data.pub_date }</span>
                </div>
                {managePart}
              </div>
          </div>
        );
      }
});

var Option = React.createClass({
  render: function() {
    return (
      <option value={this.props.value}>{this.props.text}</option>
    );
  }
});

app.CommentFormView = React.createClass({
    mixins: [BreakLine.formHelper],
    fields: {
        "text": "Comment",
        "Type": "type"
    },
    verify: function() {
        var errors = {};
        var data = this.state.model.attributes;

        if(_.isUndefined(data.text) || data.text === "")
            errors['text'] = ['This field must not be blank'];

        return errors;
    },
    getTextOption: function(action) {
        var type = getTypeFromPath();

        var results = {
            'hoshins': {
                'NO': 'Overall comment',
                'AD': 'Proposal for hoshin theme addition'
            },
            'items': {
                'NO': 'Overall comment',
                'AD': 'Proposal for concrete action addition',
                'MO': 'Comment on target',
                //'RE': 'Item removal proposal'
            },
            'concrete_actions': {
                'NO': 'Overall comment',
                //'MO': 'Implementation priority modification proposal',
                //'RE': 'Implementation priority removal proposal'
            },
            'any': {}
        };

        if(typeof action === 'undefined')
            return results[type];

        var result = results[type][action];
        if(typeof result === 'undefined')
            result = 'Default';

        return result;
    },
    save: function(event) {
        event.preventDefault();

        if(this.state.model.isNew()) {
            var url = this.props.data.url;
            var parent = url[url.length-1];
            this.state.model.attributes.parent = parseInt(parent);
        }

        this.state.model.attributes.type_parent = getTypeFromPath();
        this.saveModel();
    },
    render: function() {
        var data = this.state.model.attributes;
        var header = "Add a comment";
        if(!this.state.model.isNew())
            header = "Modify the comment";

        var text = "";
        if(!_.isUndefined(data.text))
            text = data.text;

        var type = "NO";
        if(!_.isUndefined(data.type))
            type = data.type;

        var options = this.getTextOption();
        console.log(options)
        var optionsComponents = _.map(Object.keys(options), function(key, index) {
            return <Option value={key} text={options[key]} key={index}/>;
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
                    <label htmlFor="type">Type</label>
                      <select className="form-control" data-model="type" value={type} onChange={this.valueHandleChange}>
                          { optionsComponents }
                    </select>
                  </div>

                  <div className="row form-group">
                    <label htmlFor="text">Comment</label>
                      <textarea className="form-control" data-model="text" value={text} onChange={this.valueHandleChange} rows="6" />
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

app.CommentList = br.List.extend({
    ItemView: app.CommentView,
    FormView: app.CommentFormView,
    url: app.getUrlResource('comments'),
    defaults: {
        owner:  USER
    },
    render: function (Nodes, modelForm) {
        return (
            <div>
                {Nodes}
                <this.FormView model={modelForm} data={this.data}/>
            </div>
        );
    }
});