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

(function($) {
    jQuery.fn.ulightbox = function(method) {
        // retrieves both the reference to the currently
        // matched object and the body object
        var matchedObject = this;

        var init = function() {
            if (!matchedObject.length) {
                return;
            }

            var screen = jQuery(".screen", matchedObject);
            var screens = jQuery(".screens > li", matchedObject);
            var nextButton = jQuery(".next-button", matchedObject);
            var previousButton = jQuery(".previous-button", matchedObject);

            var _screens = [];

            screens.each(function(index, element) {
                        var _element = jQuery(this);
                        var url = _element.html();
                        _screens.push(url);
                    });

            matchedObject.data("index", 0);
            matchedObject.data("screens", _screens);

            reset(matchedObject);

            nextButton.click(function() {
                        next(matchedObject);
                    });

            previousButton.click(function() {
                        previous(matchedObject);
                    });
        };

        var next = function(matchedObject) {
            var index = matchedObject.data("index");
            var screens = matchedObject.data("screens");

            if (index == screens.length - 1) {
                return;
            }
            setScreen(matchedObject, index + 1);
        };

        var previous = function(matchedObject) {
            var index = matchedObject.data("index");
            var screens = matchedObject.data("screens");

            if (index == 0) {
                return;
            }
            setScreen(matchedObject, index - 1);
        };

        var reset = function(matchedObject) {
            setScreen(matchedObject, 0);
        };

        var setScreen = function(matchedObject, index) {
            var screenIndex = jQuery(".screen-index", matchedObject);
            var screenCounter = jQuery(".screen-counter", matchedObject);
            var screens = matchedObject.data("screens");

            var screen = jQuery(".screen", matchedObject);
            var _screen = screens[index];
            screen.attr("src", _screen);
            matchedObject.data("index", index);

            screenIndex.html(String(index + 1));
            screenCounter.html(String(screens.length));
        }

        switch (method) {
            case "next" :
                next(matchedObject);
                break;

            case "previous" :
                previous(matchedObject);
                break;

            case "reset" :
                reset(matchedObject);
                break;

            default :
                init();
        }
    };
})(jQuery);

jQuery(document).ready(function() {
            var lightbox = jQuery(".lightbox");
            var buttonSignup = jQuery(".button-signup");

            lightbox.ulightbox();

            buttonSignup.click(function() {
                        // retrieves the signup form reference and resets
                        // it so that the values displayed are "erased" and the form
                        // restored to the "original" value
                        var windowSignupForm = jQuery(".window-signup form");
                        windowSignupForm.trigger("reset");
                    });
        });
