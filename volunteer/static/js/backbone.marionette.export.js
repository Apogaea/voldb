// Backbone.Marionette.Export, v2.1.1
// Copyright (c)2014 Michael Heim, Zeilenwechsel.de
// Distributed under MIT license
// http://github.com/hashchange/backbone.marionette.export

;( function( Backbone, _ ) {
    "use strict";

    /**
     * Captures all properties of an object, including the non-enumerable ones, all the way up the prototype chain.
     * Returns them as an array of property names.
     *
     * In legacy browsers which don't support Object.getOwnPropertyNames, only enumerable properties are returned.
     * There is no alternative way to list non-enumerable properties in ES3, which these browsers are based on (see
     * http://stackoverflow.com/a/8241423/508355). Listing the enumerable properties is usually good enough, though.
     * Affects IE8.
     *
     * Code lifted from the MDC docs, http://goo.gl/hw2h4G
     *
     * @param obj
     * @returns string[]
     */
    function listAllProperties ( obj ) {

        var objectToInspect,
            property,
            result = [];

        if ( Object.getPrototypeOf && Object.getOwnPropertyNames ) {

            // Modern browser. Return enumerable and non-enumerable properties, all up the prototype chain.
            for ( objectToInspect = obj; objectToInspect !== null; objectToInspect = Object.getPrototypeOf( objectToInspect ) ) {
                result = result.concat( Object.getOwnPropertyNames( objectToInspect ) );
            }

        } else {

            // Legacy browser. Return enumerable properties only, all up the prototype chain.
            for ( property in obj ) result.push( property );
        }

        return _.unique( result );
    }

    // Capture all native array properties.
    var nativeArrayProperties =  listAllProperties( [] );

    /**
     * Is called before export(). Use it to manipulate or add state before export. No-op by default, implement as
     * needed.
     */
    Backbone.Model.prototype.onBeforeExport = Backbone.Collection.prototype.onBeforeExport = function () {
        // noop by default.
    };

    /**
     * Is called after export(). No-op by default, implement as needed.
     */
    Backbone.Model.prototype.onAfterExport = Backbone.Collection.prototype.onAfterExport = function () {
        // noop by default.
    };

    /**
     * Is called on export and handed the data hash intended for export. It can manipulate or add to the data and must
     * return it afterwards.
     *
     * The method is a no-op by default, returns the data unmodified. Implement as needed.
     *
     * There is no need to call the methods which have been specified in options.export. They have already been baked
     * into properties and are part of the data hash. Rather, onExport is intended for calling methods with a arguments
     * (those can't be passed to options.export) and for more complex manipulation tasks.
     *
     * @param data
     */
    Backbone.Model.prototype.onExport = Backbone.Collection.prototype.onExport = function ( data ) {
        return data;
    };

    Backbone.Model.prototype["export"] = Backbone.Collection.prototype["export"] = function () {
        var data, exportable, conflicts, hops;

        function allowExport ( obj ) {
            return (
                obj && obj["export"] &&
                ( obj instanceof Backbone.Model || obj instanceof Backbone.Collection ) &&
                hops < obj["export"].global.maxHops
            );
        }

        hops = arguments.length ? arguments[0] : 0;

        // Before all else, run the onBeforeExport handler.
        if ( this.onBeforeExport ) this.onBeforeExport();

        // Get the Model or Collection data just like Marionette does it.
        if ( this instanceof Backbone.Collection ) {

            // Collection: Map the array of models to an array of exported model hashes. This is the only thing
            // Marionette does, out of the box, except that it calls model.toJSON for the transformation.
            //
            // We use the enhancements of model.export instead. But still, we get no more than an array of model hashes
            // at this point.
            data = this.map( function ( model ) { return allowExport( model ) ? model["export"]( hops + 1 ) : model; } );

        } else {

            // Model

            if ( _.cloneDeep ) {

                // With Lo-dash / deep-cloning ability: Deep clone the model attributes, calling export() on nested
                // Backbone models and collections in the process (up to the maximum recursion depth, then switching to
                // cloning without calls to export() ).
                data = _.cloneDeep( this.attributes, function ( attribute ) {
                    return allowExport( attribute ) ? attribute["export"]( hops + 1 ) : undefined; }
                );

            } else {

                // Model: Get the model properties for export to the template. This is the only thing Marionette does, out
                // of the box.
                data = this.toJSON();                       // this is the same as _.clone(this.attributes);

                // Call export() recursively on attributes holding a Backbone model or collection, up to the maximum
                // recursion depth.
                _.each( data, function ( attrValue, attrName, data ) {
                    if ( allowExport( attrValue ) ) data[attrName] = attrValue["export"]( hops + 1 );
                } );

            }

        }

        // Call the methods which are defined in the `exportable` property. Attach the result of each call to the
        // exported data, setting the property name to that of the method.
        if ( this.exportable ) {

            exportable = this.exportable;
            if ( ! _.isArray( exportable ) ) exportable = exportable ? [ exportable ] : [];

            _.each( exportable, function( method ) {

                var name,

                // The configuration can be read off either the Model or Collection prototype;
                // both reference the same object.
                    strictMode = this["export"].global.strict;

                if ( _.isUndefined( method ) ) throw new Error( "Can't export method. Undefined method reference" );

                if ( _.isString( method ) ) {

                    // Normalize the method name and get the method reference from the name.
                    name = method.indexOf( "this." ) === 0 ? method.substr( 5 ) : method;
                    if ( ! ( name in this ) && strictMode ) throw new Error( "Can't export \"" + name + "\". The method doesn't exist" );
                    method = this[name];

                } else {
                    throw new Error( "'exportable' property: Invalid method identifier" );
                }

                if ( _.isFunction( method )) {

                    // Call the method and turn it into a property of the exported object.
                    data[name] = method.apply( this );

                } else {

                    if ( this instanceof Backbone.Model && strictMode ) {

                        // Model: Only act on a real method. Here, `method` is a reference to an ordinary property, ie
                        // one which is not a function. Throw an error because a reference of that kind is likely to be
                        // a mistake, or else bad design.
                        //
                        // Model data must be created with Model.set and must not be handled here. It is captured by
                        // toJSON() and thus available to the templates anyway.
                        throw new Error( "'exportable' property: Invalid method identifier \"" + name + "\", does not point to a function" );

                    } else {

                        // Collection: Export an ordinary, non-function property. There isn't a native way to make a
                        // collection property available to templates, so exporting it is legit.
                        data[name] = this[name];

                    }

                }

                // Call export() recursively if the property holds a Backbone model or collection, up to the maximum
                // recursion depth.
                if ( _.cloneDeep ) {

                    // With Lo-dash / deep-cloning ability: clone other objects, too, and also call export on Backbone
                    // models or collections deeply nested within those objects.
                    data[name] = _.cloneDeep( data[name], function ( value ) {
                            return allowExport( value ) ? value["export"]( hops + 1 ) : undefined;
                    } );

                } else {
                    if ( allowExport( data[name] ) ) data[name] = data[name]["export"]( hops + 1 );
                }

                // Discard undefined values. According to the spec, valid JSON does not represent undefined values.
                if ( _.isUndefined( data[name] ) ) delete data[name];

            }, this );
        }

        // Run the onExport handler to modify/finalize the data if needed.
        if ( this.onExport ) data = this.onExport( data );

        // Trigger the onAfterExport handler just before returning.
        if ( this.onAfterExport ) this.onAfterExport();

        // Collection:
        // The exported collection is simply an array (of model hashes). But the native array object is augmented with
        // properties created by the export.
        //
        // These properties must not be allowed to overwrite native array methods or properties. Check the exported
        // property names and throw an error if they clash with the native ones.
        if ( this instanceof Backbone.Collection ) {

            conflicts = _.intersection( nativeArrayProperties,  _.keys( data ) ) ;
            if ( conflicts.length ) {
                throw new Error( "Can't export a property with a name which is reserved for a native array property. Offending properties: " + conflicts.join( ", " ) );
            }

        }

        return data;
    };

    Backbone.Model.prototype["export"].global = Backbone.Collection.prototype["export"].global = {
        maxHops: 4,
        strict: false
    };

    if ( Backbone.Marionette ) {

        Backbone.Marionette.ItemView.prototype.serializeData = Backbone.Marionette.CompositeView.prototype.serializeData = function () {
            // Largely duplicating the original serializeData() method in Marionette.ItemView, but using Model.export
            // instead of Model.toJSON as a data source if Model.export is available. Ditto for Collection.export.
            //
            // For the original code, taken from Marionette 1.0.4, see
            // https://github.com/marionettejs/backbone.marionette/blob/v1.0.4/src/marionette.itemview.js#L21

            var data = {};

            if ( this.model ) {
                data = this.model["export"] && this.model["export"]() || this.model.toJSON();
            }
            else if ( this.collection ) {
                data = { items: this.collection["export"] && this.collection["export"]() || this.collection.toJSON() };
            }

            return data;
        };

    }

}( Backbone, _ ));