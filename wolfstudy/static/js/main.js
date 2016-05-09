var TagManager = (function($) {
    var isValidTagName = function(text) {
        // Valid tag name:
        // - one or more alphanumeric characters
        // - zero or more of:
        //     - single dash
        //     - one or more alphanumeric characters
        // 
        // Valid:
        //     tag    tag123    tag-name     tag-with-multiple-words
        // Invalid:
        //     -tag    tag-    tag--name    t@g
        return /^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$/.test(text);
    }

    var showPopupMessage = function(message) {
        var tagInput = $("#add-tag-input");

        tagInput.attr({
            "data-toggle": "tooltip",
            "data-placement": "bottom",
            "data-trigger": "focus",
            "title": message
        });

        tagInput.tooltip("show");
    }

    var tagExists = function(tagname) {
        var tagFound = false;

        $(".tag", "#tags-container").each(function(index, element) {
            var currentTagname = $(element).children(".tag-text").html();
            if (currentTagname == tagname) {
                // We found a tag
                tagFound = true;

                // Break from the jQuery each loop
                return false;
            }
        });

        return tagFound;
    }

    var addTag = function() {
        // Check for adding more than 5 tags
        if ($("#tags-container > div").length >= 5) {
            showPopupMessage("Please do not add more than 5 tags.");
            return;
        }

        // Get the text of #add-tag-input
        var tagInput = $("#add-tag-input");
        var tagText = tagInput.val();

        if (isValidTagName(tagText)) {
            // Check for duplicate tags
            if (tagExists(tagText)) {
                showPopupMessage("Please do not add a duplicate tag.");
                return;
            }

            // Make a tag div:
            // <div class="tag bg-primary">
            //     <span class="tag-text">tagtext</span>
            //     <a class="remove-tag-button">
            //         <span class="glyphicon glyphicon-remove"></span>
            //     </a>
            // </div>
            var newTag = $("<div></div>")
                .append($("<span></span>")
                    .addClass("tag-text")
                    .html(tagText)
                )
                .addClass("tag bg-primary")
                .append($("<a></a>")
                    .addClass("remove-tag-button")
                    .append($("<span></span>")
                        .addClass("glyphicon glyphicon-remove")
                    )
                    .on("click", function(e) {
                        $(e.target).closest(".tag").remove();
                    })
                );

            // Add the tag div to #tags-container
            $("#tags-container").append(newTag);

            // Clear the contents of the input
            tagInput.val("");
        } else {
            showPopupMessage("Invalid tag.");
        }
    }

    var prepareTagsForSubmit = function() {
        var tags = serialize();
        $("#tags").val(tags.join(","));
    }

    var serialize = function() {
        var tags = [];

        $(".tag", "#tags-container").each(function(index, element) {
            tags.push($(element).children(".tag-text").html());
        });

        return tags;
    }

    return {
        init: function() {
            $("#add-tag-button").on("click", addTag);

            $("#add-tag-input").on("keydown", function(e) {
                $(this).tooltip("destroy");

                if (e.which == 13) {
                    addTag();
                    return false;
                }
            });

            $("#ask-question-form").on("submit", prepareTagsForSubmit);
        }
    }
})(jQuery);

jQuery(function() {
    TagManager.init();
});
