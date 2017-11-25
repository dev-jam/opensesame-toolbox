---
API: 2
OpenSesame: 3.0.7
Platform: posix
---
set width "@@4@@"
set title "@@3@@"
set synth_backend "legacy"
set subject_parity "even"
set subject_nr "0"
set start "experiment"
set sampler_backend "legacy"
set mouse_backend "@@2@@"
set keyboard_backend "@@11@@"
set height "@@5@@"
set foreground "@@1@@"
set font_size "18"
set font_italic "no"
set font_family "mono"
set font_bold "no"
set description "Default description"
set coordinates "relative"
set compensation "0"
set canvas_backend "@@2@@"
set bidi "no"
set background "@@0@@"

define sequence experiment
	set flush_keyboard yes
	set description "Runs a number of items in sequence"
	run instruction "always"
	run loop "always"

define form_multiple_choice form_multiple_choice
	set timeout "infinite"
	set spacing "10"
	set question "[question_text]"
	__options__
@@13@@
	__end__
	set margins "50;50;50;50"
	set form_var "response"
	set form_title "@@10@@"
	set description "A simple multiple choice item"
	set button_text "Ok"
	set allow_multiple "no"
	set _theme "gray"
	set advance_immediately "yes"

define form_text_display instruction
	set timeout "infinite"
	set spacing "10"
	set rows "1;4;1"
	set only_render "no"
	set ok_text "Ok"
	set margins "50;50;50;50"
	set form_title "Questionnaire Instruction"
	__form_text__
@@9@@
	__end__
	set description "A simple text display form"
	set cols "1;1;1"
	set _theme "gray"
	widget 0 0 3 1 label text="[form_title]"
	widget 0 1 3 1 label center=no text="[form_text]"
	widget 1 2 1 1 button text="[ok_text]"

define logger logger
	set use_quotes yes
	set ignore_missing yes
	set description "Logs experimental data"
	set auto_log yes

define loop loop
	set skip "0"
	set repeat "1"
	set order "@@7@@"
	set offset "no"
	set item "sequence"
	set description "Repeatedly runs another item"
	set cycles "@@6@@"
	set column_order "id;category;answer_options;answer_options_scores;question_text"
	set break_if "never"
@@12@@
	run sequence

define sequence sequence
	set flush_keyboard yes
	set description "Runs a number of items in sequence"
	run form_multiple_choice "always"
	run logger "always"
