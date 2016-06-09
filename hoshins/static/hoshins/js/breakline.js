var BreakLine = {};
var br = BreakLine;

{
    BreakLine.items = function (obj) {
        if (_.isUndefined(obj) || _.isNull(obj)) return [];

        return _.map(Object.keys(obj), function (key) {
            return [key, obj[key]];
        });
    };

    var oldSync = Backbone.sync;
    Backbone.sync = function (method, model, options) {
        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method)
            );
        }

        options.beforeSend = function (xhr, settings) {
            xhr.setRequestHeader('Authorization', 'Token ' + USER.token);
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        };

        return oldSync(method, model, options);
    };

    var Class = function () {
        this.initialize && this.initialize.apply(this, arguments);
    };

    Class.extend = function (childPrototype) {
        var parent = this;
        var child = function () {
            return parent.apply(this, arguments);
        };

        child.extend = parent.extend;
        var Surrogate = function () {};
        Surrogate.prototype = jQuery.extend(true, {}, parent.prototype);
        child.prototype = new Surrogate();

        // Create the elements dependants of the child attributes
        if (Surrogate.prototype.hasOwnProperty('__childrenExtend__') && typeof Surrogate.prototype.__childrenExtend__ == 'function') {
            for (var key in childPrototype) {
                Surrogate.prototype[key] = childPrototype[key];
            }

            Surrogate.prototype.__childrenExtend__();
        }

        for (var key in childPrototype) {
            child.prototype[key] = childPrototype[key];
        }

        return child;
    };

    BreakLine.Ul = React.createClass({
        displayName: 'Ul',

        render: function () {
            return React.createElement(
                'span',
                { className: 'tab-20' },
                ' ',
                this.props.text,
                ' ',
                React.createElement('br', null)
            );
        }
    });
    BreakLine.Error = React.createClass({
        displayName: 'Error',

        render: function () {
            var rows = [];
            for (var i = 0; i < this.props.messages.length; i++) rows.push(React.createElement(BreakLine.Ul, { text: this.props.messages[i], key: i }));

            return React.createElement(
                'div',
                { className: 'alert alert-danger', role: 'alert' },
                React.createElement('span', { className: 'glyphicon glyphicon-exclamation-sign', 'aria-hidden': 'true' }),
                React.createElement(
                    'span',
                    { className: 'tab-5' },
                    ' ',
                    this.props.fieldName,
                    ' :'
                ),
                React.createElement('br', null),
                rows
            );
        }
    });

    BreakLine.Errors = React.createClass({
        displayName: 'Errors',

        render: function () {
            var nodes = BreakLine.items(this.props.errors);
            var index = 0;

            nodes = nodes.map(function (error) {
                return React.createElement(BreakLine.Error, { fieldName: error[0], messages: error[1], key: index++ });
            });

            return React.createElement(
                'div',
                null,
                nodes
            );
        }
    });

    BreakLine.formHelper = {
        _changeModelType: function (model, isForm, isOptimistic) {
            model._isForm = isForm;
            model._isOptimistic = isOptimistic;

            model.collection.trigger('change', model);
        },
        setOptimistic: function (model) {
            model.id = "temp";
            this._changeModelType(model, false, true);
        },
        resetOptimistic: function (model) {
            this._changeModelType(model, true, false);
        },
        confirmeOptimistic: function (model) {
            this._changeModelType(model, false, false);
        },
        formatErrors: function (errors) {
            var fields = {};
            if (!_.isUndefined(this.fields)) fields = this.fields;

            for (key in errors) {
                if (key in fields) {
                    errors[fields[key]] = errors[key];
                    delete errors[key];
                }
            }

            return errors;
        },
        saveModel: function (event, success, error) {
            if (typeof event !== "undefined") event.preventDefault();

            if (typeof this.verify === "function") {
                var errors = this.verify();
                if (!_.isEmpty(errors)) {
                    this.state.model['_errors'] = this.formatErrors(errors);
                    this.state.model.collection.trigger('change', this.state.model);

                    return;
                }
            }

            var isNew = this.state.model.isNew();
            var parent = this;

            this.setOptimistic(this.state.model);
            if (isNew) this.state.model.collection.add(this.state.model);

            this.state.model.save(null, {
                error: function (model, response, options) {
                    if (isNew) model.collection.remove(model);

                    if (typeof error === "function") error(model, response, options);

                    var errors = { "Server": ["An unknown error occurred"] };

                    if (response.status == 400) errors = parent.formatErrors(response.responseJSON);else if (response.status == 0) errors = { "Server": ["The server is currently unreachable, please try it again later"] };

                    model['_errors'] = errors;
                    parent.resetOptimistic(model);
                },
                success: function (model, response, options) {
                    parent.confirmeOptimistic(model);

                    var done = function () {
                        if (isNew) {
                            parent.props = { model: parent.newModel() };
                            parent.replaceState(parent.getInitialState());
                            parent.render();

                            if (typeof parent.componentDidMount === "function") parent.componentDidMount();
                        }
                    };

                    if (typeof success === "function") $.when(success(model, response, options)).then(done);else done();

                    if (!_.isUndefined(app.router)) app.router.resetIndicators();
                }
            });
        },
        delete: function (event, success, error) {
            if (typeof event !== "undefined") event.preventDefault();
            this.props.model.destroy({
                error: function (model, response, options) {
                    if (typeof error === "function") error(model, response, options);
                },
                success: function (model, response, options) {
                    if (typeof success === "function") success(model, response, options);

                    if (!_.isUndefined(app.router)) app.router.resetIndicators();
                }
            });
        },
        modify: function (event) {
            event.preventDefault();
            this.props.model._isForm = true;
            this.props.model.trigger('change', this.props.model);
        },
        getInitialState: function () {
            return { model: this.props.model };
        },
        setAttribute: function (name, value) {
            /*
                Immutable part (best way to do), but there is a problem with the model.
                It need to be the same to stay in the collection...
                 var changement = {
                                model:{
                                    attributes:{}
                                }
                };
                changement.model.attributes[name] = {$set: value};
                 var newState = React.addons.update(this.state, changement);
                this.setState(newState);
            */
            this.state.model.attributes[name] = value;
            this.replaceState(this.state);
        },
        valueHandleChange: function (event) {
            this.setAttribute(event.target.dataset.model, event.target.value);
        }
    };

    BreakLine.List = Class.extend({
        // Params to extend
        url: undefined,

        // Params to extend to have a viewer and attach it to a dom element
        ItemView: undefined,
        el: undefined,

        // Optional
        defaults: undefined,
        render: undefined,
        FormView: undefined,

        // Params filled during the initialization
        model: undefined,
        view: undefined,

        modelForm: undefined,
        data: undefined,

        __childrenExtend__: function () {
            var parent = this;

            // Set the Item model
            var params = { urlRoot: parent.url };
            if (this.defaults) params['defaults'] = this.defaults;

            this.ItemModel = Backbone.Model.extend(params);

            this.Model = Backbone.Collection.extend({
                model: parent.ItemModel,
                url: parent.url,
                comparator: function (model) {
                    return model.id;
                },
                all: function () {
                    this.url = parent.url;
                    return this;
                },
                query: function (query) {
                    this.all();

                    query = _.map(query, function (value, key) {
                        return key + "=" + value;
                    }).join("&");

                    this.url = this.url + '?' + query;
                    return this;
                }
            });

            this.model = new this.Model();
            this.ItemModel.prototype.collection = this.model;
            this.modelForm = new this.ItemModel();
            this.fetched = true;

            if (typeof this.FormView !== "undefined") {
                this.FormView.prototype.newModel = function () {
                    return new parent.ItemModel();
                };
                this.FormView.prototype.collection = this.model;
                var oldRender = this.FormView.prototype.render;

                this.FormView.prototype.render = function () {

                    if (_.isUndefined(this.state) && typeof this.getInitialState === "function") this.replaceState(this.getInitialState());

                    if (this.state.model._isOptimistic) return React.createElement('div', null);else return oldRender.apply(this);
                };
            }
        },
        initialize: function (el) {
            this.el = el;
            var parent = this;

            /*
              * If the list is viewable (i.e if there is at least an ItemView and
              * an el), the object to do that are instantiate. Otherwise it's just
              * a skeleton to manipulate models.
              *
              */
            if (typeof this.el !== "undefined" && typeof this.ItemView !== "undefined") {
                if (!this.render) {
                    var classNameDefault = parent.url[0] == '/' ? parent.url.substring(1) : parent.url;
                    classNameDefault = classNameDefault + "List";
                    this.render = function (Nodes) {
                        return React.createElement("div", { className: classNameDefault }, Nodes);
                    };
                }

                // TODO: key depends of attributeId
                this.View = React.createClass({
                    displayName: 'View',

                    render: function () {
                        var index = 0;
                        var Nodes = this.props.data.map(function (model) {
                            var view = model._isForm ? parent.FormView : parent.ItemView;

                            index += 1;
                            return React.createElement(view, {
                                model: model,
                                key: model.id,
                                el: parent.el,
                                data: parent.data,
                                index: index
                            });
                        });
                        return parent.render(Nodes, parent.modelForm);
                    }
                });

                this._View = Backbone.View.extend({
                    initialize: function (data) {
                        this.collection = data;
                        _.bindAll(this, 'render');
                        this.collection.bind('change', this.render);
                        this.collection.bind('add', this.render);
                        this.collection.bind('remove', this.render);
                    },
                    render: function (model) {
                        ReactDOM.render(React.createElement(parent.View, { data: this.collection.models }), document.getElementById(parent.el));
                    }
                });
                this.view = new this._View(this.model);
                this.view.render();
            } else console.warn("A collection defined without viewer");
        },
        fetch: function () {
            var parent = this;

            var fetchAux = function () {
                parent.fetched = false;

                parent.model.fetch({
                    error: function (model, response) {
                        console.error('[Error ' + response.status + '] GET request to ' + model.url + " :" + '\n' + response.responseText);
                    }
                }).done(function () {
                    parent.fetched = true;
                    if (typeof parent.view !== 'undefined') parent.view.render();
                });
            };

            this.doneFetching(fetchAux);
        },
        save: function () {
            this.model.save(null, {
                error: function (model, response) {
                    console.error('[Error ' + response.status + '] PUT request to ' + model.url + " :" + '\n' + response.responseText);
                }
            });
        },
        delete: function () {
            this.model.destroy({
                error: function (model, response) {
                    console.error('[Error ' + response.status + '] DELETE request to ' + model.url + " :" + '\n' + response.responseText);
                }
            });
        },
        query: function (args) {
            this.model.query(args);
        },
        get: function (id) {
            var result = this.model.get(id);

            if (!result) {
                result = new this.ItemModel({ id: id });
            }

            return result;
        },
        doneFetching: function (func) {
            var id = setInterval(isDone, 100);
            var parent = this;

            function isDone() {
                if (parent.fetched) {
                    try {
                        func();
                    } finally {
                        clearInterval(id);
                    }
                }
            }
        },
        newItem: function (data) {
            return new this.ItemModel(data);
        }
    });
}