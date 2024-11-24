/*
Powered by ly200.com		http://www.ly200.com
广州联雅网络科技有限公司		020-83226791
*/

var global_obj={
	timer:'',
	check_form:function(notnull_obj, format_obj, type, is_new){
		var flag=false,
			is_new=(typeof(arguments[3])=='undefined')?0:1;
		if(notnull_obj){
			notnull_obj.each(function(){
				var $lang = $(this).parents('.tab_txt').attr('lang'); //后台语言版
				if(!$(this).find('input').length && $.trim($(this).val())==''){
					if($lang){ //后台语言版
						$(this).parents('.rows').find('.tab_box_btn[data-lang='+$lang+']').addClass('empty');
					}
					if($(this).attr('parent_null')){ //提示在父级
						$(this).parents('[parent_null]').css('border', '1px solid red').addClass('null');
					}else{
						$(this).css('border', '1px solid red').addClass('null');
					}
					flag==false && ($(this).focus());
					flag=true;
				}else{
					$(this).parents('.rows').find('.tab_box_btn[data-lang='+$lang+']').removeClass('empty');
					if($(this).attr('parent_null')){ //提示在父级
						$(this).parents('[parent_null]').removeAttr('style').removeClass('null');
					}else{
						$(this).removeAttr('style').removeClass('null');
					}
				}
			});
			//后台语言版
			$('.rows').find('.tab_box_row .tips').hide();
			$('.rows').find('.tab_box_row .tab_box_btn').each(function(){
				if($(this).hasClass('empty')){
					$(this).parents('.tab_box_row').find('.tips').show();
				}
			});
			if(flag){return flag;};
		}
		if(format_obj){
			var reg={
				'MobilePhone':/^1[34578]\d{9}$/,
				'Telephone':/^(0\d{2,3})(-)?(\d{7,8})(-)?(\d{3,})?$/,
				'Fax':/^(0\d{2,3})(-)?(\d{7,8})(-)?(\d{3,})?$/,
				'Email':/^\w+[a-zA-Z0-9-.+_]+@[a-zA-Z0-9-.+_]+\.\w*$/,
				'Length':/^.*/
			};
			var tips={
				'MobilePhone':lang_obj.format.mobilephone,
				'Telephone':lang_obj.format.telephone,
				'Fax':lang_obj.format.fax,
				'Email':lang_obj.format.email,
				'Length':lang_obj.format.length
			};
			if(type==1){
				format_obj.each(function(){
					var o=$(this);
					if($.trim(o.val())){
						if(reg[o.attr('format')].test($.trim(o.val()))===false){
							o.css('border', '1px solid red').addClass('null');
							o.focus();
							flag=true;
						}
					}
				});
			}else{
				format_obj.each(function(){
					var o=$(this);
					var s=o.attr('format').split('|');
					if(!$.trim(o.val())){
						flag=false;
					}else if((s[0]=='Length' && $.trim(o.val()).length!=parseInt(s[1])) || (s[0]!='Length' && reg[s[0]].test($.trim(o.val()))===false)){
						if(is_new==1){
							global_obj.new_win_alert(tips[s[0]].replace('%num%', s[1]));
						}else{
							global_obj.win_alert(tips[s[0]].replace('%num%', s[1]),'','sorry');
						}
						o.css('border', '1px solid red').addClass('null');
						o.focus();
						flag=true;
						return false;
					}
				});
			}
		}
		return flag;
	},

	win_alert:function(tips, callback, type, is_pop){
		var type=(typeof(arguments[2])=='undefined')?'alert':arguments[2],
			is_pop=(typeof(arguments[3])=='undefined')?0:1,
			html;
		$('#div_mask, .win_alert').remove();//优先清空多余的弹出框
		global_obj.div_mask();
		html='<div class="win_alert">';
			html+='<div class="win_close"><button class="close">X</button></div>';
			if(type=='password'){
				html+='<div class="win_pwd clean"><div class="pwd_name fl">'+lang_obj.signIn.password+':</div><div class="fl pwd_r"><input name="Password" value="" type="password" autocomplete="off" class="pwd_text"><div class="error_tips"></div></div></div>';
			}else if(type=='sorry'){
				html+='<div class="win_top_tips">'+lang_obj.global.sorry+'</div>';
				html+='<div class="win_tips">'+tips+'</div>';
			}else{
				html+='<div class="win_tips">'+tips+'</div>';
			}
			html+='<div class="win_btns"><button class="btn btn_sure">'+lang_obj.global.confirm+'</button>';
			if(type=='confirm' || type=='password') html+='<button class="btn btn_cancel">'+lang_obj.global.cancel+'</button>';
			html+='</div>';
		html+='</div>';
		$('body').prepend(html);
		$('.win_alert').css({left:$(window).width()/2-$('.win_alert').outerWidth()/2,top:'30%'});
		if(type=='confirm'){
			$('.win_alert').delegate('.close, .btn_cancel', 'click', function(){
				$('.win_alert').remove();
				is_pop==0 && global_obj.div_mask(1);
			}).delegate('.btn_sure', 'click', function(){
				$.isFunction(callback) && callback();
				$('.win_alert .close').click();
			});
			/*$(document).keyup(function(event){	//Esc、Space取消提示，空格、Enter确定提示
				if(event.keyCode==27 || event.keyCode==8){
					$('.win_alert .close').click();
				}else if(event.keyCode==32 || event.keyCode==13){
					$.isFunction(callback) && callback();
					$('.win_alert .close').click();
				}
			});*/
		}else if(type=='password'){
			$('.win_alert').on('click', '.close, .btn_cancel', function(){
				$('.win_alert').remove();
				global_obj.div_mask(1);
			}).on('click', '.btn_sure', function(){
				$.isFunction(callback) && callback();
				//$('.win_alert .close').click();
			});
		}else{
			$('.win_alert').delegate('.close, .btn_sure', 'click', function(){
				$.isFunction(callback) && callback();
				$('.win_alert').remove();
				is_pop==0 && global_obj.div_mask(1);
			});
			/*$(document).keyup(function(event){	//Esc、Enter、Space、空格取消提示
				if(event.keyCode==13 || event.keyCode==8 || event.keyCode==27 || event.keyCode==32) {
					$('.win_alert .close').click();
				}
			});*/
		}
		return false;
	},

	new_win_alert:function(tips, callback, type, is_pop, status, btn){ //status => await(叹号) fail(红叉)
		var type=(typeof(arguments[2])=='undefined')?'alert':arguments[2],
			is_pop=(typeof(arguments[3])=='undefined')?0:1,
			status=(typeof(arguments[4])=='undefined')?'await':arguments[4],
			btn=(typeof(arguments[5])=='undefined')?lang_obj.global.confirm:arguments[5],
			html;
		$('#div_mask, .new_win_alert').remove();//优先清空多余的弹出框
		global_obj.div_mask();
		html='<div class="new_win_alert">';
			html+='<div class="win_close"><button class="close"></button></div>';
			html+='<div class="win_tips"><i class="icon_success_status '+status+'"></i>'+tips+'</div>';
			html+='<div class="win_btns">';
				if(type=='confirm') html+='<button class="btn btn_cancel">'+lang_obj.global.cancel+'</button>';
				html+='<button class="btn btn_sure">'+btn+'</button>';
			html+='<div class="clear"></div>';
			html+='</div>';
		html+='</div>';
		$('body').prepend(html);
		$('.new_win_alert').css({left:$(window).width()/2-$('.new_win_alert').outerWidth()/2,top:'30%'});
		if(type=='confirm'){
			$('.new_win_alert').delegate('.close, .btn_cancel', 'click', function(){
				$('.new_win_alert').remove();
				is_pop==0 && global_obj.div_mask(1);
			}).delegate('.btn_sure', 'click', function(){
				$.isFunction(callback) && callback();
				$('.new_win_alert .close').click();
			});
			/*$(document).keyup(function(event){	//Esc、Space取消提示，空格、Enter确定提示
				if(event.keyCode==27 || event.keyCode==8){
					$('.new_win_alert .close').click();
				}else if(event.keyCode==32 || event.keyCode==13){
					$.isFunction(callback) && callback();
					$('.new_win_alert .close').click();
				}
			});*/
		}else{
			$('.new_win_alert').delegate('.close, .btn_sure', 'click', function(){
				$.isFunction(callback) && callback();
				$('.new_win_alert').remove();
				is_pop==0 && global_obj.div_mask(1);
			});
			/*$(document).keyup(function(event){	//Esc、Enter、Space、空格取消提示
				if(event.keyCode==13 || event.keyCode==8 || event.keyCode==27 || event.keyCode==32) {
					$('.win_alert .close').click();
				}
			});*/
		}
		return false;
	},

	win_alert_auto_close:function(tips, status, time, pos_top, no_remove_mask){ //status => await(叹号) fail(红叉)
		var status=(typeof(arguments[1])=='undefined')?'await':arguments[1],
			time=(typeof(arguments[2])=='undefined' || !arguments[2])?'2000':arguments[2],
			pos_top=(typeof(arguments[3])=='undefined' || !arguments[3])?'40%':arguments[3],
			no_remove_mask=(typeof(arguments[4])=='undefined')?1:arguments[4],
			html="";
		if(no_remove_mask) $('#div_mask, .new_win_alert').remove();//优先清空多余的弹出框
		if(status!='loading' || (status=='loading' && time==-1)){
			//除了loading Or 固定显示loading
			html+='<div class="new_win_alert win_alert_auto_close'+(status=='loading'?' win_alert_loading':'')+'">';
			html+=	'<div class="win_tips"><i class="icon_success_status '+status+'"></i>'+tips+'</div>';
			html+='</div>';

			$('body').prepend(html);
			$('.new_win_alert').css({left:$(window).width()/2-$('.new_win_alert').outerWidth()/2, top:pos_top});
		}
		clearTimeout(global_obj.timer);
		if(status!='loading' || (status=='loading' && time>=0)){
			//除了loading Or 计时自动关闭loading
			global_obj.timer=setTimeout(function(){
				$('.new_win_alert').remove();
			}, time);
		}
		return false;
	},

	div_mask:function(remove){
		if(remove==1){
			$('#div_mask').remove();
		}else{
			if(!$('#div_mask').size()){
				$('body').prepend('<div id="div_mask"></div>');
				$('#div_mask').css({width:'100%', height:$(document).height(), overflow:'hidden', position:'fixed', top:0, left:0, background:'#000', opacity:0.6, 'z-index':10000});
			}
		}
	},

	data_posting:function(display, tips){
		if(display){
			$('body').prepend('<div id="data_posting"><img src="../images/ico/data_posting.gif" width="16" height="16" align="absmiddle" />  '+tips+'</div>');
			$('#data_posting').css({
				width:'188px',
				height:'24px',
				'line-height':'24px',
				padding:'0 8px',
				overflow:'hidden',
				border:'1px solid #bbb',
				background:'#ddd',
				position:'fixed',
				top:'40%',
				left:'48%',
				'z-index':10001
			});
		}else{
			setTimeout('$("#data_posting").remove();', 500);
		}
	},

	urlencode:function(str) {
		str = (str + '').toString();
		return encodeURIComponent(str).replace(/!/g, '%21').replace(/'/g, '%27').replace(/\(/g, '%28').replace(/\)/g, '%29').replace(/\*/g, '%2A').replace(/%20/g, '+');
	},

	in_array:function(needle, arr){
		for(var i=0; i<arr.length && arr[i]!=needle; i++);
		return !(i==arr.length);
	},

	is_array:function(data){
		if(Object.prototype.toString.call(data) == '[object Array]'){
			return true;
		}else{
			return false;
		}
	},
	
	setCookie:function(name, value, expiredays){
		var exdate=new Date();
		exdate.setDate(exdate.getDate()+expiredays);
		alert(name+"="+escape(value)+((expiredays==null) ? "" : ";expires="+exdate.toGMTString()));
		document.cookie=name+"="+escape(value)+((expiredays==null) ? "" : ";expires="+exdate.toGMTString());
	},
	
	getCookie:function(name){
		if(document.cookie.length>0){
			start=document.cookie.indexOf(name+"=");
			if(start!=-1){
				start=start+(name.length+1);
				end=document.cookie.indexOf(";", start);
				if(end==-1) end=document.cookie.length;
				return unescape(document.cookie.substring(start, end));
			}
		}
		return "";
	},
	
	delCookie:function(name, expiredays){
		var exdate=new Date();
		exdate.setDate(exdate.getDate()-1);
		var value=global_obj.getCookie(name)
		if(value){
			document.cookie=name+"="+escape(value)+((expiredays==null) ? "" : ";expires="+exdate.toGMTString());
		}
	}
}

//Object => string
$.toJSON = typeof JSON == "object" && JSON.stringify ? JSON.stringify: function(e) {
	if (e === null) return "null";
	var t, n, r, i, s = $.type(e);
	if (s === "undefined") return undefined;
	if (s === "number" || s === "boolean") return String(e);
	if (s === "string") return $.quoteString(e);
	if (typeof e.toJSON == "function") return $.toJSON(e.toJSON());
	if (s === "date") {
		var o = e.getUTCMonth() + 1,
		u = e.getUTCDate(),
		a = e.getUTCFullYear(),
		f = e.getUTCHours(),
		l = e.getUTCMinutes(),
		c = e.getUTCSeconds(),
		h = e.getUTCMilliseconds();
		o < 10 && (o = "0" + o);
		u < 10 && (u = "0" + u);
		f < 10 && (f = "0" + f);
		l < 10 && (l = "0" + l);
		c < 10 && (c = "0" + c);
		h < 100 && (h = "0" + h);
		h < 10 && (h = "0" + h);
		return '"' + a + "-" + o + "-" + u + "T" + f + ":" + l + ":" + c + "." + h + 'Z"'
	}
	t = [];
	if ($.isArray(e)) {
		for (n = 0; n < e.length; n++) t.push($.toJSON(e[n]) || "null");
		return "[" + t.join(",") + "]"
	}
	if (typeof e == "object") {
		for (n in e) if (hasOwn.call(e, n)) {
			s = typeof n;
			if (s === "number") r = '"' + n + '"';
			else {
				if (s !== "string") continue;
				r = $.quoteString(n)
			}
			s = typeof e[n];
			if (s !== "function" && s !== "undefined") {
				i = $.toJSON(e[n]);
				t.push(r + ":" + i)
			}
		}
		return "{" + t.join(",") + "}"
	}
};

//string => Object
$.evalJSON = typeof JSON == "object" && JSON.parse ? JSON.parse: function(str) {
	return eval("(" + str + ")")
};