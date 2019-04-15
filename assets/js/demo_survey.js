var demoSurvey = {
	maybeLoadSurvey: function(config) {
	    if (config.advanced.includeDemographicSurvey) {
	        console.log("loading demo survey");
	        $('#demo-survey').load("assets/html/demo_survey.html");
	        $('#demo-survey').hide();
	        $('#feedback-field').hide();
	    }
	},
	hideSurvey: function() {
		$('#demo-survey').hide();
	},
	showTask: function() {
		
		// make sure to hide experiment: use the appropriate div references (or add div wrappers) to hide the previous task elements
		//$('#custom-experiment').hide();
		$(".subtask").hide();
		// -----------------------
		
		$('#demo-survey').show();

        // Rules for collecting demographic survey data
        $('#survey-form')
          .form({
            fields: {
                gender: {
                    identifier: 'gender',
                    rules: [{
                        type: 'checked',
                        prompt: 'Please select a gender'
                    }]
                }, 
                ageGroup: {
                    identifier: 'ageGroup',
                    rules: [{
                        type: 'checked',
                        prompt: 'Please select an age group'
                    }]
                }, 
                ethnicity: {
                    identifier: 'ethnicity',
                    rules: [{
                        type: 'checked',
                        prompt: 'Please select an ethnicity'
                    }]
                }, 
                education: {
                    identifier: 'education',
                    rules: [{
                        type: 'checked',
                        prompt: 'Please select an education level'
                    }]
                }, 
                vizExperience: {
                    identifier: 'vizExperience',
                    rules: [{
                        type: 'checked',
                        prompt: 'Please select your experience with visualizations'
                    }]
                }
            }
        });

        $("input:checkbox[name=ethnicity]").change(function() {
            var unspecified = $("#ethnicUnspecified").is(":checked");
            if (unspecified) {
                $("input:checkbox[name=ethnicity]").not("#ethnicUnspecified")
                    .prop("checked", false);
                $(".ethnicityOption").addClass("disabled");
            } else {
                $(".ethnicityOption").removeClass("disabled");
            }
        });
	},
	collectData: function() {
	    var gender = $("input[type=radio][name=gender]:checked").val();
	    var ageGroup = $("input[type=radio][name=ageGroup]:checked").val();
	    var ethnicity = $("input[type=checkbox][name=ethnicity]:checked").val();
	    var education = $("input[type=radio][name=education]:checked").val();
	    var vizExperience = $("input[type=radio][name=vizExperience]:checked").val();
	    var feedback = htmlEscape($("textarea[name=feedback]").val());

	    var data = {
	        gender: gender,
	        ageGroup: ageGroup,
	        ethnicity: ethnicity,
	        education: education,
	        vizExperience: vizExperience,
	        feedback: feedback
	    }; 

        return {
            survey_data: data
        }; 
	},
	validateTask: function() {
		console.log("validating demographic survey");
		$('#survey-form').form('validate form');
		// falsey value indicates no error...
		if (!$('#survey-form').form('is valid')) {
			return {errorMessage: ""}
		}
		return false;
	}
}

function htmlEscape(str) {
  /* Html-escape a sensitive string. */
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}