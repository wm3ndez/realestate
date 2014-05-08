/*! Django Superformset - v1.0.3 - 2014-04-16
* https://github.com/jgerigmeyer/jquery-django-superformset
* Based on jQuery Formset 1.1r14, by Stanislaus Madueke
* Original Portions Copyright (c) 2009 Stanislaus Madueke
* Modifications Copyright (c) 2014 Jonny Gerig Meyer; Licensed BSDv3 */
(function ($) {

  'use strict';

  var methods = {
    init: function (options) {
      var vars = {};
      var opts = vars.opts = $.extend({}, $.fn.superformset.defaults, options);
      var wrapper = vars.wrapper = $(this);
      var rows = vars.rows = wrapper.find(opts.rowSel);
      var container = vars.container = rows.closest(opts.containerSel);
      vars.totalForms = wrapper
        .find('input[id$="' + opts.prefix + '-TOTAL_FORMS"]');
      vars.maxForms = wrapper
        .find('input[id$="' + opts.prefix + '-MAX_NUM_FORMS"]');

      // Clone the form template to generate new form instances
      var tpl = vars.tpl = container.find(opts.formTemplate).clone(true);
      container.find(opts.formTemplate).find('[required], .required')
        .removeAttr('required').removeData('required-by').addClass('required');
      tpl.removeAttr('id').find('input, select, textarea').filter('[required]')
        .addClass('required').removeAttr('required');

      // Add delete-trigger and insert-above-trigger (if applicable) to template
      methods.addDeleteTrigger(tpl, opts.canDelete, vars);
      methods.addInsertAboveTrigger(tpl, vars);

      // Iterate over existing rows...
      rows.each(function () {
        var thisRow = $(this);
        // Add delete-trigger and insert-above-trigger to existing rows
        methods.addDeleteTrigger(
          thisRow,
          (opts.canDelete && !opts.deleteOnlyNew),
          vars
        );
        methods.addInsertAboveTrigger(thisRow, vars);
        // Attaches handlers watching for changes to inputs,
        // ...to add/remove ``required`` attr
        methods.watchForChangesToOptionalIfEmptyRow(thisRow, vars);
      });

      // Unless using auto-added rows, add and/or activate trigger to add rows
      if (!opts.autoAdd) {
        methods.activateAddTrigger(vars);
      }

      // Add extra empty row, if applicable
      if (opts.alwaysShowExtra && opts.autoAdd) {
        methods.autoAddRow(vars);
        wrapper.closest('form').submit(function () {
          $(this).find(opts.rowSel).filter('.extra-row')
            .find('input, select, textarea').each(function () {
              $(this).removeAttr('name');
            }
          );
        });
      }

      return wrapper;
    },

    activateAddTrigger: function (vars) {
      var opts = vars.opts;
      var addButton;
      if (vars.wrapper.find(opts.addTriggerSel).length) {
        addButton = vars.addButton = vars.wrapper.find(opts.addTriggerSel);
      } else {
        addButton = vars.addButton = $(opts.addTrigger).appendTo(vars.wrapper);
      }
      // Hide the add-trigger if we've reach the maxForms limit
      if (!methods.showAddButton(vars)) { addButton.hide(); }
      addButton.click(function (e) {
        var trigger = $(this);
        var formCount = parseInt(vars.totalForms.val(), 10);
        var newRow = vars.tpl.clone(true).addClass('new-row');
        newRow.find('input, select, textarea').filter('.required')
          .attr('required', 'required');
        if (opts.addAnimationSpeed) {
          newRow.hide().insertAfter(vars.wrapper.find(opts.rowSel).last())
            .animate(
              {'height': 'toggle', 'opacity': 'toggle'},
              opts.addAnimationSpeed
            );
        } else {
          newRow.insertAfter(vars.wrapper.find(opts.rowSel).last()).show();
        }
        newRow.find('input, select, textarea, label').each(function () {
          methods.updateElementIndex($(this), opts.prefix, formCount);
        });
        // Attaches handlers watching for changes to inputs,
        // ...to add/remove ``required`` attr
        methods.watchForChangesToOptionalIfEmptyRow(newRow, vars);
        vars.totalForms.val(formCount + 1);
        // Check if we've exceeded the maximum allowed number of forms:
        if (!methods.showAddButton(vars)) { trigger.hide(); }
        // If a post-add callback was supplied, call it with the added form:
        if (opts.addedCallback) { opts.addedCallback(newRow); }
        e.preventDefault();
      });
    },

    // Attaches handlers watching for changes to inputs,
    // ...to add/remove ``required`` attr
    watchForChangesToOptionalIfEmptyRow: function (row, vars) {
      var opts = vars.opts;
      if (opts.optionalIfEmpty && row.is(opts.optionalIfEmptySel)) {
        var inputs = row.find('input, select, textarea');
        inputs.filter('[required], .required').removeAttr('required')
          .data('required-by', opts.prefix).addClass('required');
        row.data('original-vals', inputs.serialize());
        inputs.not(opts.deleteTriggerSel).change(function () {
          methods.updateRequiredFields(row, vars);
        });
      }
    },

    // Replace ``-__prefix__`` with correct index in for, id, name attrs
    updateElementIndex: function (elem, prefix, ndx) {
      var idRegex = new RegExp('(' + prefix + '-(\\d+|__prefix__))');
      var replacement = prefix + '-' + ndx;
      if (elem.attr('for')) {
        elem.attr('for', elem.attr('for').replace(idRegex, replacement));
      }
      if (elem.attr('id')) {
        elem.attr('id', elem.attr('id').replace(idRegex, replacement));
      }
      if (elem.attr('name')) {
        elem.attr('name', elem.attr('name').replace(idRegex, replacement));
      }
    },

    // Check whether we can add more rows
    showAddButton: function (vars) {
      return (
        vars.maxForms.val() === '' ||
        (vars.maxForms.val() - vars.totalForms.val() > 0)
      );
    },

    // Add delete trigger to end of a row, or activate existing delete-trigger
    addDeleteTrigger: function (row, canDelete, vars) {
      var opts = vars.opts;
      if (canDelete) {
        // Add a delete-trigger to remove the row from the DOM
        $(opts.deleteTrigger).appendTo(row).click(function (e) {
          var thisRow = $(this).closest(opts.rowSel);
          var rows, i;
          var updateSequence = function (rows, i) {
            rows.eq(i).find('input, select, textarea, label').each(function () {
              methods.updateElementIndex($(this), opts.prefix, i);
            });
          };
          var removeRow = function () {
            thisRow.remove();
            // Update the TOTAL_FORMS count:
            rows = vars.wrapper.find(opts.rowSel);
            vars.totalForms.val(rows.not('.extra-row').length);
            // Update names and IDs for all child controls,
            // ...so they remain in sequence.
            for (i = 0; i < rows.length; i = i + 1) {
              updateSequence(rows, i);
            }
            // If a post-delete callback was provided, call it with deleted form
            if (opts.removedCallback) { opts.removedCallback(thisRow); }
          };
          if (opts.removeAnimationSpeed) {
            $.when(
              thisRow.animate(
                {'height': 'toggle', 'opacity': 'toggle'},
                opts.removeAnimationSpeed
              )
            ).done(removeRow);
          } else {
            removeRow();
          }
          e.preventDefault();
        });
      } else {
        // If we're dealing with an inline formset,
        // ...just remove :required attrs when marking a row deleted
        row.find(opts.deleteTriggerSel).change(function () {
          var trigger = $(this);
          var thisRow = trigger.closest(opts.rowSel);
          if (trigger.prop('checked')) {
            thisRow.addClass(opts.deletedRowClass);
            thisRow.find('[required]').removeAttr('required')
              .addClass('deleted-required');
            // If a post-delete callback was provided, call it with deleted form
            if (opts.removedCallback) { opts.removedCallback(thisRow); }
          } else {
            thisRow.removeClass(opts.deletedRowClass);
            thisRow.find('.deleted-required').attr('required', 'required')
              .removeClass('deleted-required');
          }
        });
      }
    },

    // Add insert-above trigger before a row, if ``insertAboveTrigger: true``
    addInsertAboveTrigger: function (row, vars) {
      var opts = vars.opts;
      if (opts.insertAbove) {
        $(opts.insertAboveTrigger).prependTo(row).click(function (e) {
          var thisRow = $(this).closest(opts.rowSel);
          var formCount = parseInt(vars.totalForms.val(), 10);
          var newRow = vars.tpl.clone(true).addClass('new-row');
          var rows, i;
          var updateSequence = function (rows, i) {
            rows.eq(i).find('input, select, textarea, label').each(function () {
              methods.updateElementIndex($(this), opts.prefix, i);
            });
          };
          newRow.find('input, select, textarea').filter('.required')
            .attr('required', 'required');
          if (opts.addAnimationSpeed) {
            newRow.hide().insertBefore(thisRow).animate(
              {'height': 'toggle', 'opacity': 'toggle'}, opts.addAnimationSpeed
            );
          } else {
            newRow.insertBefore(thisRow).show();
          }
          // Update the TOTAL_FORMS count:
          rows = vars.wrapper.find(opts.rowSel);
          vars.totalForms.val(formCount + 1);
          // Update names and IDs for child controls so they remain in sequence.
          for (i = 0; i < rows.length; i = i + 1) {
            updateSequence(rows, i);
          }
          // Attaches handlers watching for changes to inputs,
          // ...to add/remove ``required`` attr
          methods.watchForChangesToOptionalIfEmptyRow(newRow, vars);
          // Check if we've exceeded the maximum allowed number of rows:
          if (!methods.showAddButton(vars)) { $(this).hide(); }
          // If a post-add callback was supplied, call it with the added form:
          if (opts.addedCallback) { opts.addedCallback(newRow); }
          $(this).blur();
          e.preventDefault();
        });
      }
    },

    // Add a row automatically
    autoAddRow: function (vars) {
      var opts = vars.opts;
      var formCount = parseInt(vars.totalForms.val(), 10);
      var newRow = vars.tpl.clone(true);
      var rows = vars.wrapper.find(opts.rowSel);
      if (opts.addAnimationSpeed) {
        newRow.hide().css('opacity', 0).insertAfter(rows.last())
          .addClass('extra-row').animate(
            {'height': 'toggle', 'opacity': '0.5'},
            opts.addAnimationSpeed
          );
      } else {
        newRow.css('opacity', 0.5).insertAfter(rows.last())
          .addClass('extra-row');
      }
      // When the extra-row receives focus...
      newRow.find('input, select, textarea, label').one('focus', function () {
        var el = $(this);
        var thisRow = el.closest(opts.rowSel);
        // fade it in
        thisRow.removeClass('extra-row').css('opacity', 1);
        // add "required" to appropriate inputs if not an "optionalIfEmpty" row
        if (
          el.hasClass('required') &&
          !(opts.optionalIfEmpty && newRow.is(opts.optionalIfEmptySel))
        ) {
          el.attr('required', 'required');
        }
        // update the totalForms count
        vars.totalForms.val(
          vars.wrapper.find(opts.rowSel).not('.extra-row').length
        );
        // fade in the delete-trigger
        if (opts.deleteOnlyActive) {
          thisRow.find(opts.deleteTriggerSel).fadeIn();
        }
        // and auto-add another extra-row
        if (
          methods.showAddButton(vars) &&
          thisRow.is(vars.wrapper.find(opts.rowSel).last())
        ) {
          methods.autoAddRow(vars);
        }
      }).each(function () {
        var el = $(this);
        methods.updateElementIndex(el, opts.prefix, formCount);
        el.filter('[required]').removeAttr('required').addClass('required');
      });
      // Attaches handlers watching for changes to inputs,
      // ...to add/remove ``required`` attr
      methods.watchForChangesToOptionalIfEmptyRow(newRow, vars);
      // Hide the delete-trigger initially, if ``deleteOnlyActive: true``
      if (opts.deleteOnlyActive) {
        newRow.find(opts.deleteTriggerSel).hide();
      }
      // If a post-add callback was supplied, call it with the added form
      if (opts.addedCallback) { opts.addedCallback(newRow); }
    },

    // Check if inputs have changed from original state,
    // ...and update ``required`` attr accordingly
    updateRequiredFields: function (row, vars) {
      var opts = vars.opts;
      var inputs = row.find('input, select, textarea');
      var relevantInputs = inputs.filter(function () {
        return $(this).data('required-by') === opts.prefix;
      });
      var state = inputs.serialize();
      var originalState = row.data('original-vals');
      if (state === originalState) {
        relevantInputs.removeAttr('required');
      } else {
        relevantInputs.filter('.required').not('.deleted-required')
          .attr('required', 'required');
      }
    },

    // Expose internal methods to allow stubbing in tests
    exposeMethods: function () {
      return methods;
    }
  };

  $.fn.superformset = function (method) {
    if (methods[method]) {
      return methods[method].apply(
        this,
        Array.prototype.slice.call(arguments, 1)
      );
    } else if (typeof method === 'object' || !method) {
      return methods.init.apply(this, arguments);
    } else {
      $.error('Method ' + method + ' does not exist on jQuery.superformset');
    }
  };

  /* Setup plugin defaults */
  $.fn.superformset.defaults = {
    prefix: 'form',               // The form prefix for your django formset
    containerSel: 'form',         // Container selector
                                  // ...(must contain rows and formTemplate)
    rowSel: '.dynamic-form',      // Selector to match each row in a formset
    formTemplate: '.empty-form .dynamic-form',
                                  // Selector for empty form template to be
                                  // ...cloned to generate new form instances
                                  // ...Must be outside element on which formset
                                  // ...is called, but within containerSel
    deleteTrigger: '<a href="#" class="remove-row" title="remove">remove</a>',
                                  // The HTML "remove" link added to the end of
                                  // ...each form-row (if ``canDelete: true``)
    deleteTriggerSel: '.remove-row',
                                  // Selector for HTML "remove" links
                                  // ...Used to target existing delete-trigger,
                                  // ...or to target ``deleteTrigger``
    addTrigger: '<a href="#" class="add-row" title="add">add</a>',
                                  // The HTML "add" link added to the end of all
                                  // ...forms if no ``addTriggerSel``
    addTriggerSel: null,          // Selector for trigger to add a new row
                                  // ...Used to target existing trigger
                                  // ...if provided, ``addTrigger`` is ignored
    addedCallback: null,          // Fn called each time a new form row is added
    removedCallback: null,        // Fn called each time a form row is deleted
    deletedRowClass: 'deleted',   // Add to deleted row if ``canDelete: false``
    addAnimationSpeed: 'normal',  // Speed (ms) to animate adding rows
                                  // ...If false, new rows appear w/o animation
    removeAnimationSpeed: 'fast', // Speed (ms) to animate removing rows
                                  // ...If false, new rows disappear w/o anim.
    autoAdd: false,               // If true, the "add" link will be removed,
                                  // ...and a row will be automatically added
                                  // ...when text is entered in the final
                                  // ...textarea of the last row
    alwaysShowExtra: false,       // If true, an extra (empty) row will always
                                  // ...be displayed (req. ``autoAdd: true``)
    deleteOnlyActive: false,      // If true, extra empty rows cannot be removed
                                  // ...until they acquire focus
                                  // ...(requires ``alwaysShowExtra: true``)
    canDelete: false,             // If false, rows cannot be removed from DOM.
                                  // ...``deleteTriggerSel`` will remove
                                  // ...``required`` attr from fields within a
                                  // ..."deleted" row.
                                  // ...deleted rows should be hidden via CSS
    deleteOnlyNew: false,         // If true, only newly-added rows can be
                                  // ...deleted (requires ``canDelete: true``)
    insertAbove: false,           // If true, ``insertAboveTrigger`` will be
                                  // ...added to the end of each form-row
    insertAboveTrigger:
      '<a href="#" class="insert-row" title="insert">insert</a>',
                                  // The HTML "insert" link add to the end of
                                  // ...each row (req. ``insertAbove: true``)
    optionalIfEmpty: true,        // If true, required fields in a row will be
                                  // ...optional until changed from initial vals
    optionalIfEmptySel: '[data-empty-permitted="true"]'
                                  // Selector for rows to apply optionalIfEmpty
                                  // ...logic (req. ``optionalIfEmpty: true``)
  };
}(jQuery));