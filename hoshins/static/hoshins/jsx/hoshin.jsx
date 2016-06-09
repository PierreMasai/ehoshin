var app = app || {};

function changeHoshin(model) {
    url = ['', TEAM_NAME, model.attributes.id];
    app.router.navigate(url.join('/') , {trigger:true});
}

app.HoshinItemView = React.createClass({
    mixins: [br.formHelper],
    changeHoshin: function(event) {
        event.preventDefault();
        changeHoshin(this.props.model);
    },
    del: function(event) {
            var deleted = function() {
                app.router.navigate('/' + TEAM_NAME , {trigger:true});
            };
        
            this.delete(event, deleted);
    },
    render: function() {
        var data = this.props.model.attributes;
        var managePart = "";
        var size = "col-sm-12";
        if(USER.isModerator) {
            managePart = <app.Toogler model={this.props.model} classe_names="col-sm-1"
                                      right={true} deleteHandler={this.del} />;
            size = "col-sm-11";
        }

        return (
          <div className="row">
              <div className="col-sm-12 hoshin_menu_box">
                  <a className={size + " show"} href='#' onClick={this.changeHoshin}>
                    <button className="btn flat btn-default hoshins_items" aria-label="Left Align">
                        <span style={{backgroundColor: data.color}}>
                            &nbsp;
                        </span>
                        <span>{data.name}</span>
                    </button>
                  </a>
                  {managePart}
              </div>
          </div>
        );
    }
});

app.HoshinFormView = React.createClass({
    mixins: [BreakLine.formHelper],
    fields: {
        "name": "Name"
    },
    verify: function() {
        var errors = {};
        var data = this.state.model.attributes;

        if(_.isUndefined(data.name) || data.name === "")
            errors['name'] = ['This field must not be blank'];

        return errors;
    },
    bgHandleChange: function(event) {
        this.setAttribute("color", event.color.toHex());
    },
    componentDidMount: function() {
        var DOMNode = ReactDOM.findDOMNode(this);
        $(DOMNode).find(".color")
                  .colorpicker({format: "hex"})
                  .on('changeColor.colorpicker', this.bgHandleChange);
    },
    save: function(event) {
        this.saveModel(event, changeHoshin);
    },
    render: function() {
        var data = this.state.model.attributes;
        var style = {
            backgroundColor: data.color
        };

        var className = "row";
        if(this.props.model._isOptimistic)
            className += " isOptimistic";

        return (
            <div className={className}>
                <div className="col-sm-12">
                    <span type="button" className="btn flat btn-default" aria-label="Left Align">
                        <BreakLine.Errors errors={this.state.model._errors} />
                        <div className="input-group">
                            <span className="input-group-addon color"><i className="add-on" style={style}>&nbsp;&nbsp;&nbsp;&nbsp;</i></span>
                            <input type="text" className="form-control " data-model="name" placeholder="Name" value={data.name} onChange={this.valueHandleChange} />
                            <a className="input-group-addon" href="#" onClick={this.save}>
                                Save
                             </a>
                        </div>
                    </span>
                </div>
          </div>
        );
    }
});

app.HoshinList = br.List.extend({
    ItemView: app.HoshinItemView,
    FormView: app.HoshinFormView,
    url: app.getUrlResource('hoshins'),
    defaults: {
        color:  "#81b9c3",
        owner:  USER
    },
    render: function (Nodes, modelForm) {
        var formPart = "";

        if(USER.isModerator)
            formPart = <this.FormView model={modelForm}/>;

        return (
            <div>
                {Nodes}
                {formPart}
            </div>
        );
    }
});

app.HoshinIndicator = React.createClass({
    render: function() {
        var style = {
            backgroundColor: this.props.color
        };
        return (
          <div className="indicator panel panel-default">
              <div className="panel-heading indicator_part without_border" style={style}>
                <img src={ICONS_URL + this.props.picture_name} height="30" />
              </div>
              <div className="panel-body indicator_part">
                  <div className="span6 center">
                    <span>{this.props.value}</span>
                  </div>
              </div>
          </div>
        );
      }
});


app.HoshinIndicatorList = React.createClass({
    render: function() {
        return (
            <table className="table">
                <tbody>
                    <tr>
                        <td>Themes</td><td>{this.props.nb_items}</td>
                    </tr>
                    <tr>
                        <td>Concrete actions</td><td>{this.props.nb_implementation_priorities}</td>
                    </tr>
                    <tr>
                        <td>Comments</td><td>{this.props.nb_comments}</td>
                    </tr>
                    <tr>
                        <td>Users</td>
                        <td>{this.props.nb_users}</td>
                    </tr>
                    <tr>
                        <td>Users who commented once</td>
                        <td>{this.props.nb_commentators}</td>
                    </tr>
                    <tr>
                        <td>Users who commented more than once</td>
                        <td>{this.props.nb_chatty_commentators}</td>
                    </tr>
                </tbody>
            </table>
        );
      }
});
