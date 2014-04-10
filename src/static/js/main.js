// Hive Pingu System
// Copyright (C) 2008-2012 Hive Solutions Lda.
//
// This file is part of Hive Pingu System.
//
// Hive Pingu System is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Hive Pingu System is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Hive Pingu System. If not, see <http://www.gnu.org/licenses/>.

// __author__    = João Magalhães <joamag@hive.pt>
// __version__   = 1.0.0
// __revision__  = $LastChangedRevision$
// __date__      = $LastChangedDate$
// __copyright__ = Copyright (c) 2010-2012 Hive Solutions Lda.
// __license__   = GNU General Public License (GPL), Version 3

(function(jQuery) {
    jQuery.fn.uheroku = function() {
        // retrieves both the reference to the currently
        // matched object and the body object
        var matchedObject = this;
        var _body = jQuery("body")

        // in case there are currently no matched objects
        // no need to continue with the processing
        if (matchedObject.length = 0) {
            return;
        }

        // retrieves the height of the currently matched object
        // and the top margin of the body (to be updated)
        var height = matchedObject.outerHeight(true);
        var marginTop = _body.css("margin-top")
        marginTop = parseInt(marginTop);

        // increments the margin top of the body and sets it in
        // the current body object
        marginTop = marginTop + height;
        _body.css("margin-top", marginTop + "px");
    };
})(jQuery);

(function(jQuery) {
    jQuery.fn.uapply = function(options) {
        // sets the jquery matched object
        var matchedObject = this;

        // tries to retrieves the heroku navigation bar
        // and runs the jeroku extension on it
        var herokuNav = jQuery(".heroku-nav", matchedObject);
        herokuNav.uheroku();
    };
})(jQuery);

jQuery(document).ready(function() {
            var _body = jQuery("body");
            _body.bind("applied", function(event, base) {
                        base.uapply();
                    });
        });
