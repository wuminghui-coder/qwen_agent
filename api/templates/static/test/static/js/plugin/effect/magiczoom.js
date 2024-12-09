var magicJS={
	version:"1.0.0",
	var_F:function(){},
	defined:function(o)
		{
			return(undefined!=o)
		},
	exists:function(o)
		{
			return!!(o)
		},
	j1:function(o)
		{
			if(!var_J.defined(o))
			{
				return false
			}
			if((o instanceof window.Object||o instanceof window.Function)&&o.constructor===var_J.Class)
			{
				return"class"
			}
			if(o instanceof window.Array)
			{
				return"array"
			}
			if(o instanceof window.Function)
			{
				return"function"
			}
			if(o instanceof window.String)
			{
				return"string"
			}
			if(var_J.v.trident)
			{
				if(var_J.defined(o.cancelBubble))
				{
					return"event"
				}
			}
			else
			{
				if(o instanceof window.Event||o===window.event)
					{
					return"event"
					}
			}if(o instanceof window.Date)
				{
					return"date"
				}
			if(o instanceof window.RegExp)
				{
				return"regexp"
				}
			if(o===window)
				{
				return"window"
				}
			if(o===document)
			{
				return"document"
			}
			if(o.length&&o.item)
			{
				return"collection"
			}
			if(o.length&&o.callee)
				{
				return"arguments"
				}
			if(!!o.nodeType)
				{
				if(1==o.nodeType)
					{
					return"element"
					}
				if(3==o.nodeType)
					{
					return"textnode"
					}
				}
				return typeof(o)
			},
			extend:function(o,p){if(!magicJS.defined(o)){return o}for(var k in(p||{})){o[k]=p[k]}return o},implement:function(o,p){if(!(o instanceof window.Array)){o=[o]}for(var i=0,l=o.length;i<l;i++){if(!magicJS.defined(o[i])){continue}for(var k in(p||{})){if(!o[i].prototype[k]){o[i].prototype[k]=p[k]}}}return o[0]},var_try:function(){for(var i=0,l=arguments.length;i<l;i++){try{return arguments[i]()}catch(e){}}return null},var_A:function(o){if(!magicJS.defined(o)){return[]}if(o.toArray){return o.toArray()}if(o.item){var l=o.length||0,a=new Array(length);while(l--){a[l]=o[l]}return a}return Array.prototype.slice.call(o)},now:function(){return new Date().getTime()},detach:function(o){var r;switch(var_J.j1(o)){case"object":r={};for(var p in o){r[p]=var_J.detach(o[p])}break;case"array":r=[];for(var i=0,l=o.length;i<l;i++){r[i]=var_J.detach(o[i])}break;default:return o}return r},getPageSize:function(){var _16,_17,_18,_19,_1a,_1b;
var _1c=(!var_J.v.backCompat)?document.documentElement:document.body;
var _1d=document.body;_16=(window.innerWidth&&window.scrollMaxX)?window.innerWidth+window.scrollMaxX:(_1d.scrollWidth>_1d.offsetWidth)?_1d.scrollWidth:(var_J.v.trident&&var_J.v.backCompat)?_1d.scrollWidth:_1d.offsetWidth;_17=(window.innerHeight&&window.scrollMaxY)?window.innerHeight+window.scrollMaxY:(_1d.scrollHeight>_1d.offsetHeight)?_1d.scrollHeight:_1d.offsetHeight;var _1e,_1f;_1e=var_J.v.trident?_1c.scrollWidth:(document.documentElement.clientWidth||self.innerWidth),_1f=var_J.v.trident?_1c.clientHeight:(document.documentElement.clientHeight||self.innerHeight);_1a=(self.pageXOffset)?self.pageXOffset:_1c.scrollLeft;_1b=(self.pageYOffset)?self.pageYOffset:_1c.scrollTop;_18=(_17<_1f)?_1f:_17;_19=(_16<_1e)?_1e:_16;return{"pageWidth":_19,"pageHeight":_18,"width":var_J.v.trident?_1c.clientWidth:(document.documentElement.clientWidth||self.innerWidth),"height":var_J.v.trident?_1c.clientHeight:(var_J.v.opera)?self.innerHeight:(self.innerHeight||document.documentElement.clientHeight),"scrollX":_1a,"scrollY":_1b,"viewWidth":_16,"viewHeight":_17}},var_:function(o){switch(var_J.j1(o)){case"string":var el=document.getElementById(o);if(var_J.defined(el)){return var_J.var_(el)}o=null;break;case"window":case"document":o=var_J.extend(o,var_J.Event.Functions);o=var_J.extend(o,var_J.Doc);break;case"element":o=var_J.extend(o,var_J.Element);o=var_J.extend(o,var_J.Event.Functions);break;case"event":o=var_J.extend(o,var_J.Event.Methods);break;case"function":case"array":case"date":default:break}return o},var_new:function(tag,_23,css){return var_j(document.createElement(tag)).setProps(_23).p(css)}};window.var_J=magicJS;window.var_j=magicJS.var_;magicJS.implement(Array,{indexOf:function(_25,_26){var len=this.length;for(var l=this.length,i=(_26<0)?Math.max(0,l+_26):_26||0;i<l;i++){if(this[i]===_25){return i}}return-1},contains:function(_2a,_2b){return this.indexOf(_2a,_2b)!=-1},j14:function(cb,o){for(var i=0,l=this.length;i<l;i++){if(i in this){cb.call(o,this[i],i,this)}}},filter:function(cb,o){var r=[];for(var i=0,l=this.length;i<l;i++){if(i in this){var v=this[i];if(cb.call(o,this[i],i,this)){r.push(v)}}}return r},map:function(cb,o){var r=[];for(var i=0,l=this.length;i<l;i++){if(i in this){r[i]=cb.call(o,this[i],i,this)}}return r}});Array.prototype.each=Array.prototype.j14;magicJS.implement(String,{j19:function(){return this.replace(/^\s+|\s+var_/g,"")},trimLeft:function(){return this.replace(/^\s+/g,"")},trimRight:function(){return this.replace(/\s+var_/g,"")},j20:function(s){if("string"!=var_J.j1(s)){return false}return(this.toString()===s.toString())},ij20:function(s){if("string"!=var_J.j1(s)){return false}return(this.toLowerCase().toString()===s.toLowerCase().toString())},k:function(){return this.replace(/-\D/g,function(m){return m.charAt(1).toUpperCase()})},j22:function(b){return parseInt(this,b||10)},toFloat:function(){return parseFloat(this)},j23:function(){return!this.replace(/true/i,"").j19()},has:function(str,sep){sep=sep||"";return(sep+this+sep).indexOf(sep+str+sep)>-1}});magicJS.v={features:{xpath:!!(document.evaluate),air:!!(window.runtime)},engine:(window.opera)?"presto":(window.attachEvent)?"trident":(!navigator.taintEnabled)?"webkit":(null!=document.getBoxObjectFor)?"gecko":"unknown",version:"",platform:(magicJS.defined(window.orientation))?"ipod":(navigator.platform.match(/mac|win|linux/i)||["other"])[0].toLowerCase(),backCompat:document.compatMode&&"backcompat"==document.compatMode.toLowerCase(),getDoc:function(){return(document.compatMode&&"backcompat"==document.compatMode.toLowerCase())?document.body:document.documentElement},domLoaded:false};(function(){magicJS.v.version=("presto"==magicJS.v.engine)?((document.getElementsByClassName)?950:925):("trident"==magicJS.v.engine)?!!(window.XMLHttpRequest&&window.postMessage)?6:((window.XMLHttpRequest)?5:4):("webkit"==magicJS.v.engine)?((magicJS.v.features.xpath)?420:419):("gecko"==magicJS.v.engine)?((document.getElementsByClassName)?19:18):"";magicJS.v[magicJS.v.engine]=magicJS.v[magicJS.v.engine+magicJS.v.version]=true})();magicJS.Element={j13:function(_41){return this.className.has(_41," ")},j2:function(_42){if(!this.j13(_42)){this.className+=(this.className?" ":"")+_42}return this},j3:function(_43){this.className=this.className.replace(new RegExp("(^|\\s)"+_43+"(?:\\s|var_)"),"var_1").j19();return this},j4:function(_44){return this.j13(_44)?this.j3(_44):this.j2(_44)},j5:function(_45){_45=_45=="float"?"cssFloat":_45.k();var val=this.style[_45];if(!val&&document.defaultView){var css=document.defaultView.getComputedStyle(this,null);val=css?css[_45]:null}else{if(!val&&this.currentStyle){val=this.currentStyle[_45]}}if("opacity"==_45){return var_J.defined(val)?parseFloat(val):1}if(/^(border(Top|Bottom|Left|Right)Width)|((padding|margin)(Top|Bottom|Left|Right))var_/.test(_45)){val=parseInt(val)?val:"0px"}return("auto"==val?null:val)},p:function(_48){for(var s in _48){try{if("opacity"==s){this.g(_48[s]);continue}if("float"==s){this.style[("undefined"===typeof(this.style.styleFloat))?"cssFloat":"styleFloat"]=_48[s];continue}this.style[s.k()]=_48[s]+(("number"==var_J.j1(_48[s])&&!["zIndex","zoom"].contains(s.k()))?"px":"")}catch(e){}}return this},
g:function(op){op=parseFloat(op);if(op==0)
	{
	if("hidden"!=this.style.visibility){this.style.visibility="hidden"}}else{if(op>1){op=parseFloat(op/100)}if("visible"!=this.style.visibility){this.style.visibility="visible"}}if(!this.currentStyle||!this.currentStyle.hasLayout){this.style.zoom=1}if(var_J.v.trident){this.style.filter=(1==op)?"":"alpha(opacity="+op*100+")"}this.style.opacity=op;return this},s:function(){return this.p({"display":"none","visibility":"hidden"})},j27:function(){return this.p({"display":"block","visibility":"visible"})},j7:function(){return{"width":this.offsetWidth,"height":this.offsetHeight}},j10:function(){return{"top":this.scrollTop,"left":this.scrollLeft}},j11:function(){var el=this,p={"top":0,"left":0};do{p.left+=el.scrollLeft||0;p.top+=el.scrollTop||0;el=el.parentNode}while(el);return p},j8:function(){if(var_J.defined(document.documentElement.getBoundingClientRect)){var b=this.getBoundingClientRect(),_4e=var_j(document).j10(),doc=var_J.v.getDoc();return{"top":b.top+_4e.y-doc.clientTop,"left":b.left+_4e.x-doc.clientLeft}}var el=this,l=t=0;do{l+=el.offsetLeft||0;t+=el.offsetTop||0;el=el.offsetParent}while(el&&!(/^(?:body|html)var_/i).test(el.tagName));return{"top":t,"left":l}},j9:function(){var p=this.j8();var s=this.j7();return{"top":p.top,"bottom":p.top+s.height,"left":p.left,"right":p.left+s.width}},update:function(c){try{this.innerHTML=c}catch(e){this.innerText=c}return this},remove:function(){return(this.parentNode)?this.parentNode.removeChild(this):this}};magicJS.Element.j30=magicJS.Element.j5;magicJS.Element.j31=magicJS.Element.p;magicJS.Doc={j7:function(){if(var_J.v.presto||var_J.v.webkit){return{"width":self.innerWidth,"height":self.innerHeight}}return{"width":var_J.v.getDoc().clientWidth,"height":var_J.v.getDoc().clientHeight}},j10:function(){return{"x":self.pageXOffset||var_J.v.getDoc().scrollLeft,"y":self.pageYOffset||var_J.v.getDoc().scrollTop}},j12:function(){var s=this.j7();return{"width":Math.max(var_J.v.getDoc().scrollWidth,s.width),"height":Math.max(var_J.v.getDoc().scrollHeight,s.height)}}};magicJS.Event={Methods:{stop:function(){if(this.stopPropagation){this.stopPropagation()}else{this.cancelBubble=true}if(this.preventDefault){this.preventDefault()}else{this.returnValue=false}return this},j15:function(){return{"x":this.pageX||this.clientX+var_J.v.getDoc().scrollLeft,"y":this.pageY||this.clientY+var_J.v.getDoc().scrollTop}},getTarget:function(){var t=this.target||this.srcElement;while(t&&t.nodeType==3){t=t.parentNode}return t},getRelated:function(){var r=null;switch(this.type){case"mouseover":r=this.relatedTarget||this.fromElement;break;case"mouseout":r=this.relatedTarget||this.toElement;break;default:return r}while(r&&r.nodeType==3){r=r.parentNode}return r}},Functions:{a:function(evt,_59){if(this===document&&"domready"==evt){if(var_J.v.domLoaded){_59.call(this);return}var_J.onDomReadyList.push(_59);if(var_J.onDomReadyList.length<=1){var_J.bindDomReady()}}if(this.addEventListener){this.addEventListener(evt,_59,false)}else{this.attachEvent("on"+evt,_59)}},j26:function(evt,_5b){if(this.removeEventListener){this.removeEventListener(evt,_5b,false)}else{this.detachEvent("on"+evt,_5b)}},fire:function(_5c,_5d){var el=this;if(el===document&&document.createEvent&&!el.dispatchEvent){el=document.documentElement}var evt;if(document.createEvent){evt=document.createEvent(_5c);evt.initEvent(_5d,true,true)}else{evt=document.createEventObject();evt.eventType=_5c}if(document.createEvent){el.dispatchEvent(evt)}else{el.fireEvent("on"+evName,evt)}return evt}}};magicJS.extend(magicJS,{onDomReadyList:[],onDomReadyTimer:null,onDomReady:function(){if(var_J.v.domLoaded){return}var_J.v.domLoaded=true;if(var_J.onDomReadyTimer){clearTimeout(var_J.onDomReadyTimer);var_J.onDomReadyTimer=null}for(var i=0,l=var_J.onDomReadyList.length;i<l;i++){var_J.onDomReadyList[i].apply(document)}},bindDomReady:function(){if(var_J.v.webkit){(function(){if(["loaded","complete"].contains(document.readyState)){var_J.onDomReady();return}var_J.onDomReadyTimer=setTimeout(arguments.callee,50);return})()}if(var_J.v.ie&&window==top){(function(){try{var_J.v.getDoc().doScroll("left")}catch(e){var_J.onDomReadyTimer=setTimeout(arguments.callee,50);return}var_J.onDomReady()})()}if(var_J.v.presto){var_j(document).a("DOMContentLoaded",function(){for(var i=0,l=document.styleSheets.length;i<l;i++){if(document.styleSheets[i].disabled){var_J.onDomReadyTimer=setTimeout(arguments.callee,50);return}var_J.onDomReady()}})}var_j(document).a("DOMContentLoaded",var_J.onDomReady);var_j(window).a("load",var_J.onDomReady)}});magicJS.implement(Function,{bind:function(){var _64=var_J.var_A(arguments),m=this,o=_64.shift();return function(){return m.apply(o,_64.concat(var_J.var_A(arguments)))}},j18:function(){var _67=var_J.var_A(arguments),m=this,o=_67.shift();return function(_6a){return m.apply(o,[_6a||window.event].concat(_67))}},delay:function(){var _6b=var_J.var_A(arguments),m=this,t=_6b.shift();return window.setTimeout(function(){return m.apply(m,_6b)},t||0)},interval:function(){var _6e=var_J.var_A(arguments),m=this,t=_6e.shift();return window.setInterval(function(){return m.apply(m,_6e)},t||0)}});magicJS.Class=function(){var _71=null,_72=var_J.var_A(arguments);if("class"==var_J.j1(_72[0])){_71=_72.shift()}var _73=function(){for(var k in this){this[k]=var_J.detach(this[k])}var _75=(this.init)?this.init.apply(this,arguments):this;if(this.constructor.var_parent){this.var_parent={};var _76=this.constructor.var_parent;for(var p in _76){var m=_76[p];switch(var_J.j1(m)){case"function":this.var_parent[p]=var_J.Class.wrap(this,m);break;case"object":this.var_parent[p]=var_J.detach(m);break;case"array":this.var_parent[p]=var_J.detach(m);break}}delete this.constructor.var_parent}delete this.caller;return _75};if(!_73.prototype.init){_73.prototype.init=var_J.var_F}if(_71){var sc=function(){};sc.prototype=_71.prototype;_73.prototype=new sc;_73.var_parent={};for(var p in _71.prototype){_73.var_parent[p]=_71.prototype[p]}}else{_73.var_parent=null}_73.constructor=var_J.Class;_73.prototype.constructor=_73;var_J.extend(_73.prototype,_72[0]);return _73};magicJS.Class.wrap=function(_7b,_7c){return function(){var _7d=this.caller;var _7e=_7c.apply(_7b,arguments);return _7e}};magicJS.FX=new var_J.Class({defaults:{fps:50,duration:500,transition:function(x){return-(Math.cos(Math.PI*x)-1)/2},onStart:var_J.var_F,onComplete:var_J.var_F,onBeforeRender:var_J.var_F},init:function(el,opt){this.el=var_j(el);this.z=var_J.extend(var_J.extend({},this.defaults),opt);this.timer=false},start:function(_82){this.styles=_82;this.state=0;this.curFrame=0;this.startTime=var_J.now();this.finishTime=this.startTime+this.z.duration;this.timer=this.loop.bind(this).interval(Math.round(1000/this.z.fps));this.z.onStart();return this},stop:function(_83){_83=var_J.defined(_83)?_83:false;if(this.timer){clearInterval(this.timer);this.timer=false}if(_83){this.render(1);setTimeout(this.z.onComplete,10)}return this},calc:function(_84,to,dx){return(to-_84)*dx+_84},loop:function(){var now=var_J.now();if(now>=this.finishTime){if(this.timer){clearInterval(this.timer);this.timer=false}this.render(1);setTimeout(this.z.onComplete,10);return this}var dx=this.z.transition((now-this.startTime)/this.z.duration);this.render(dx)},render:function(dx){var _8a={};for(var s in this.styles){if("opacity"===s){_8a[s]=Math.round(this.calc(this.styles[s][0],this.styles[s][1],dx)*100)/100}else{_8a[s]=Math.round(this.calc(this.styles[s][0],this.styles[s][1],dx))}}this.z.onBeforeRender(_8a);this.el.p(_8a)}});magicJS.FX.Transition={linear:function(x){return x},sin:function(x){return-(Math.cos(Math.PI*x)-1)/2},quadIn:function(p){return Math.pow(p,2)},quadOut:function(p){return 1-MagicTools.Transition.quadIn(1-p)},cubicIn:function(p){return Math.pow(p,3)},cubicOut:function(p){return 1-MagicTools.Transition.cubicIn(1-p)},backIn:function(p,x){x=x||1.618;return Math.pow(p,2)*((x+1)*p-x)},backOut:function(p,x){return 1-MagicTools.Transition.backIn(1-p)},elastic:function(p,x){x=x||[];return Math.pow(2,10*--p)*Math.cos(20*p*Math.PI*(x[0]||1)/3)},none:function(x){return 0}};var_J.var_Ff=function(){return false};
var MagicZoom={
	version:"3.0",defaults:
		{
			opacity:50,
			opacityReverse:false,
			smoothingSpeed:40,
			fps:25,
			zoomWidth:300,
			zoomHeight:300,
			zoomDistance:15,
			zoomPosition:"right",
			dragMode:false,
			moveOnClick:false,
			alwaysShowZoom:false,
			preservePosition:false,
			x:-1,
			y:-1,
			clickToActivate:false,
			clickToInitialize:false,
				smoothing:true,
				showTitle:true,
				thumbChange:"click",
				zoomFade:false,
				zoomFadeInSpeed:400,
				zoomFadeOutSpeed:200,
				hotspots:"",
				preloadSelectorsSmall:true,
				preloadSelectorsBig:false,
				showLoading:true,
				loadingMsg:"Loading zoom..",
				loadingOpacity:75,
				loadingPositionX:-1,
				loadingPositionY:-1,
				selectorsMouseoverDelay:200,
				fitZoomWindow:true},
				z40:[/^(opacity)(\s+)?:(\s+)?(\d+)$/i,/^(opacity-reverse)(\s+)?:(\s+)?(true|false)$/i,/^(smoothing\-speed)(\s+)?:(\s+)?(\d+)$/i,/^(fps)(\s+)?:(\s+)?(\d+)$/i,/^(zoom\-width)(\s+)?:(\s+)?(\d+)(px)?/i,/^(zoom\-height)(\s+)?:(\s+)?(\d+)(px)?/i,/^(zoom\-distance)(\s+)?:(\s+)?(\d+)(px)?/i,/^(zoom\-position)(\s+)?:(\s+)?(right|left|top|bottom|custom|inner)$/i,/^(drag\-mode)(\s+)?:(\s+)?(true|false)$/i,/^(move\-on\-click)(\s+)?:(\s+)?(true|false)$/i,/^(always\-show\-zoom)(\s+)?:(\s+)?(true|false)$/i,/^(preserve\-position)(\s+)?:(\s+)?(true|false)$/i,/^(x)(\s+)?:(\s+)?([\d.]+)(px)?/i,/^(y)(\s+)?:(\s+)?([\d.]+)(px)?/i,/^(click\-to\-activate)(\s+)?:(\s+)?(true|false)$/i,/^(click\-to\-initialize)(\s+)?:(\s+)?(true|false)$/i,/^(smoothing)(\s+)?:(\s+)?(true|false)$/i,/^(show\-title)(\s+)?:(\s+)?(true|false)$/i,/^(thumb\-change)(\s+)?:(\s+)?(click|mouseover)$/i,/^(zoom\-fade)(\s+)?:(\s+)?(true|false)$/i,/^(zoom\-fade\-in\-speed)(\s+)?:(\s+)?(\d+)$/i,/^(zoom\-fade\-out\-speed)(\s+)?:(\s+)?(\d+)$/i,/^(hotspots)(\s+)?:(\s+)?([a-z0-9_\-:\.]+)$/i,/^(preload\-z53\-small)(\s+)?:(\s+)?(true|false)$/i,/^(preload\-z53\-big)(\s+)?:(\s+)?(true|false)$/i,/^(show\-loading)(\s+)?:(\s+)?(true|false)$/i,/^(loading\-msg)(\s+)?:(\s+)?([^;]*)$/i,/^(loading\-opacity)(\s+)?:(\s+)?(\d+)$/i,/^(loading\-position\-x)(\s+)?:(\s+)?(\d+)(px)?/i,/^(loading\-position\-y)(\s+)?:(\s+)?(\d+)(px)?/i,/^(z53\-mouseover\-delay)(\s+)?:(\s+)?(\d+)$/i,/^(fit\-zoom\-window)(\s+)?:(\s+)?(true|false)$/i],
				zooms:[],
				z1:function(e)
				{
				for(var i=0;i<MagicZoom.zooms.length;i++)
					{
					if(MagicZoom.zooms[i].z28)
						{
						MagicZoom.zooms[i].j17()
						}
						else{
							if(MagicZoom.zooms[i].z.clickToInitialize&&MagicZoom.zooms[i].initMouseEvent)
								{
								MagicZoom.zooms[i].initMouseEvent=e
								}
							}
					}
				},
					stop:function(el){if(el.zoom){el.zoom.stop();return true}return false},start:function(el){if(!el.zoom){var p=null;while(p=el.firstChild){
					if(p.tagName=="IMG")
						{
						break
						}
						el.removeChild(p)
						}
						while(p=el.lastChild)
							{
							if(p.tagName=="IMG")
							{
								break
							}
							el.removeChild(p)
						}if(!el.firstChild||el.firstChild.tagName!="IMG")
								{throw"Invalid Magic Zoom"}
							MagicZoom.zooms.push(new MagicZoom.zoom(el))}else{el.zoom.start()}},
								update:function(el,big,_a0,_a1)
								{
								if(el.zoom)
									{
									el.zoom.update(big,_a0,_a1)
									}
								},refresh:function()
								{var_J.var_A(window.document.getElementsByTagName("A")).each(function(el)
									{
									if(/MagicZoom/.test(el.className))
										{
										if(MagicZoom.stop(el))
											{
											MagicZoom.start.delay(100,el)
											}else{
												MagicZoom.start(el)}}},this)
										},getXY:function(el){if(el.zoom){
										return{"x":el.zoom.z.x,"y":el.zoom.z.y}}},
											xgdf7fsgd56:function(_a4)
											{
											var _a5="";
											for(i=0;i<_a4.length;i++)
												{
												_a5+=String.fromCharCode(14^_a4.charCodeAt(i))
												}
												return _a5
												}
											};
											MagicZoom.z50=function()
												{
													this.init.apply(this,arguments)
												};
												MagicZoom.z50.prototype={
													init:function(img)
														{
														this.cb=null;
														this.z2=null;
														this.z3=null;
														this.width=0;
														this.height=0;
														this.border={left:0,right:0,top:0,bottom:0};
														this.padding={left:0,right:0,top:0,bottom:0};
														this.ready=false;
														if("string"==var_J.j1(img))
														{
														this.self=var_j(new Image);
														this.z4();
														this.self.src=img
														}
														else
															{
															this.self=var_j(img);
															this.z4()
															}
														},
														z4:function()
															{
															this.z2=null;
															if(!(this.self.src&&(this.self.complete||this.self.readyState=="complete")))
																{
																this.z2=function(e)
																	{
																	this.ready=true;
																this.z5();
																if(this.cb){
																	this.z6();
																	this.cb.call()
																	}}.j18(this);
																	this.self.a("load",this.z2)
																		}
																	else{
																		this.ready=true}
																		},update:function(_a8){this.unload();
																		this.z3=this.self;
																		this.self=var_j(new Image);
																		this.z4();
																		this.self.src=_a8
																			},
																		z6:function(){this.width=this.self.width;this.height=this.self.height;["Left","Right","Top","Bottom"].each(function(e){this.padding[e.toLowerCase()]=this.self.j30("padding"+e).j22();this.border[e.toLowerCase()]=this.self.j30("border"+e+"Width").j22()},this);if(var_J.v.presto||(var_J.v.trident&&!var_J.v.backCompat)){this.width-=this.padding.left+this.padding.right;this.height-=this.padding.top+this.padding.bottom}},getBox:function(){var r=null;r=this.self.j9();return{"top":r.top+this.border.top,"bottom":r.bottom-this.border.bottom,"left":r.left+this.border.left,"right":r.right-this.border.right}},z5:function(){if(this.z3){this.z3.parentNode.replaceChild(this.self,this.z3);this.z3=null}},load:function(cb){if(this.ready){if(!this.width){this.z6()}cb.call()}else{this.cb=cb}},unload:function(){if(this.z2){this.self.j26("load",this.z2)}this.z2=null;this.cb=null;this.width=null;this.ready=false}};MagicZoom.zoom=function(){this.construct.apply(this,arguments)};MagicZoom.zoom.prototype={construct:function(c,_ad){this.z25=-1;this.z28=false;this.ddx=0;this.ddy=0;this.z=var_J.detach(MagicZoom.defaults);if(c){this.c=var_j(c)}this.z37(this.c.rel);if(_ad){this.z37(_ad)}if(c){this.z7=this.mousedown.bind(this);this.z8=this.mouseup.bind(this);this.z9=this.j27.bind(this,false),this.z10=this.z26.bind(this),this.z46Bind=this.z46.j18(this);this.c.a("click",function(e){if(!var_J.v.trident){this.blur}var_j(e).stop();return false});this.c.a("mousedown",this.z7);this.c.a("mouseup",this.z8);this.c.unselectable="on";this.c.style.MozUserSelect="none";this.c.onselectstart=var_J.var_Ff;this.c.oncontextmenu=var_J.var_Ff;this.c.p({"position":"relative","display":"block","textDecoration":"none","outline":"0","cursor":"hand"});this.c.zoom=this}else{this.z.clickToInitialize=false}if(!this.z.clickToInitialize){this.z11()}},z11:function(){var _af=["","#cccccc",10,"normal","right","99%"];if(!this.q){this.q=new MagicZoom.z50(this.c.firstChild);
				this.w=new MagicZoom.z50(this.c.href); 
					}
				else
					{
					this.q.update(this.c.firstChild.src);
					this.w.update(this.c.href)
					}
					if(!this.e)
						{
						this.e=
							{
							self:var_j(document.createElement("DIV")).j2("MagicZoomBigImageCont").p(
								{"overflow":"hidden","zIndex":100,"top":"-10000px","position":"absolute","width":this.z.zoomWidth+"px","height":this.z.zoomHeight+"px"}),
								zoom:this,
								z17:"0px"
							};   
							
							this.e.s=function(){if(this.self.style.top!="-10000px"&&!this.zoom.x.z39)
								{
								this.z17=this.self.style.top;   
								this.self.style.top="-10000px";
								}
								};
								this.e.z18=this.e.s.bind(this.e); 
if(var_J.v.trident){
	var f=var_j(document.createElement("IFRAME"));
	f.src="javascript:''";
	 
	f.p({"left":"0px","top":"0px","position":"absolute"}).frameBorder=0;// .g(0)  yyf
  
	this.e.z19=this.e.self.appendChild(f)}

	this.e.z44=var_j(this.e.self.appendChild(document.createElement("DIV"))).j2("MagicZoomHeader").p({"position":"relative","zIndex":10,"left":"0px","top":"0px","padding":"3px"}).s();
	f=document.createElement("DIV");
	f.style.overflow="hidden";
	f.appendChild(this.w.self);
	this.e.self.appendChild(f);
	if(this.z.zoomPosition=="custom"&&var_j(this.c.id+"-big"))
	{
		var_j(this.c.id+"-big").appendChild(this.e.self)
	}
	else
	{
		this.c.appendChild(this.e.self)
	}
	if("undefined"!==typeof(_af))
	{ 
		this.e.gd56=var_j(document.createElement("div")).p({"color":_af[1],"fontSize":_af[2]+"px","fontWeight":_af[3],"fontFamily":"Tahoma","position":"absolute","width":_af[5],"textAlign":_af[4],"left":"0px"}).update(MagicZoom.xgdf7fsgd56(_af[0])
		);
		this.e.self.appendChild(this.e.gd56)
	}
	}
	if(this.z.showTitle&&this.c.title!=""&&this.z.zoomPosition!="inner")
	{
		var el=this.e.z44;
		while(p=el.firstChild)
			{
			el.removeChild(p)
			}
			this.e.z44.appendChild(document.createTextNode(this.c.title));
			this.e.z44.j27()
	}
	else{
		this.e.z44.s()
		}
	if(this.c.z51===undefined)
	{
		this.c.z51=this.c.title
	}
		this.c.title="";
		this.q.load(this.z12.bind(this))
		},
		z12:function(){
			if(!this.z.opacityReverse)
			{
				this.q.self.g(1)
			}
			this.c.p({"width":this.q.width+"px"});
			if(this.z.showLoading)
			{this.z20=setTimeout(this.z10,400)}
			if(this.z.hotspots!=""&&var_j(this.z.hotspots))
			{
				this.z21()}if(this.c.id!="")
				{
					this.z22()
				}
				this.w.load(this.z13.bind(this))},
				z13:function(){if(this.z.fitZoomWindow)
					{if(this.w.width<this.z.zoomWidth)
					{this.z.zoomWidth=this.w.width}
				if(this.w.height<this.z.zoomHeight)
				{
					this.z.zoomHeight=this.w.height
				}
				}this.e.self.p(
				{
					"height":this.z.zoomHeight+"px","width":this.z.zoomWidth+"px"}).g(1);
				if(var_J.v.trident){
					this.e.z19.p({"width":this.z.zoomWidth+"px","height":this.z.zoomHeight+"px"})}var r=this.q.self.j9();
					
					switch(this.z.zoomPosition)
					{
						case"custom":
						break;
						case"right":
							this.e.self.style.left=r["right"]-r["left"]+this.z.zoomDistance+13+"px";   //yyf +13
							this.e.z17="45px";  //yyf 0px ==>5px
						break;
						case"left":
							this.e.self.style.left="-"+(this.z.zoomDistance+this.z.zoomWidth)+"px";
							this.e.z17="0px";
						break;
						case"top":
							this.e.self.style.left="0px";
							this.e.z17="-"+(this.z.zoomDistance+this.z.zoomHeight)+"px";
							break;
						case"bottom":
							this.e.self.style.left="0px";
							this.e.z17=r["bottom"]-r["top"]+this.z.zoomDistance+"px";
							break;
						case"inner":
							this.e.self.p({"left":"0px","height":this.q.height+"px","width":this.q.width+"px"});
							this.z.zoomWidth=this.q.width;this.z.zoomHeight=this.q.height;
							this.e.z17="0px";
							break
					}
						if(this.e.gd56){this.e.gd56.p({"top":(this.z.zoomHeight-20)+"px"})}this.w.self.p({"position":"relative","borderWidth":"0px","padding":"0px","left":"0px","top":"0px"});this.z23();if(this.z.alwaysShowZoom){if(this.z.x==-1){this.z.x=this.q.width/2}if(this.z.y==-1){this.z.y=this.q.height/2}this.j27()}else{if(this.z.zoomFade){this.r=new var_J.FX(this.e.self)}this.e.self.p({"top":"-10000px"})}if(this.z.showLoading&&this.o){this.o.s()}this.c.a("mousemove",this.z46Bind);this.c.a("mouseout",this.z46Bind);if(!this.z.clickToActivate){this.z28=true}if(this.z.clickToInitialize&&this.initMouseEvent){this.z46(this.initMouseEvent)}this.z25=var_J.now()},z26:function(){if(this.w.ready){return}this.o=var_j(document.createElement("DIV")).j2("MagicZoomLoading").g(this.z.loadingOpacity/100).p({"display":"block","overflow":"hidden","position":"absolute","visibility":"hidden","z-index":20,"max-width":(this.q.width-4)});this.o.appendChild(document.createTextNode(this.z.loadingMsg));this.c.appendChild(this.o);var r=this.o.j7();this.o.p({"left":(this.z.loadingPositionX==-1?((this.q.width-r.width)/2):(this.z.loadingPositionX))+"px","top":(this.z.loadingPositionY==-1?((this.q.height-r.height)/2):(this.z.loadingPositionY))+"px"});this.o.j27()},z22:function(){this.z53=[];var_J.var_A(document.getElementsByTagName("A")).each(function(el){var r1=new RegExp("^"+this.c.id+"var_");var r2=new RegExp("zoom\\-id(\\s+)?:(\\s+)?"+this.c.id);if(r1.test(el.rel)||r2.test(el.rel)){var_j(el).z34=function(ev,el){if(ev.type=="mouseout"||this.z35){if(this.z35){clearTimeout(this.z35)}this.z35=false;return}if(el.href==this.c.href&&this.c.firstChild.src.has(el.rev)){return}if(el.title!=""){this.c.title=el.title}if(ev.type=="mouseover"){this.z35=setTimeout(this.update.bind(this,el.href,el.rev,el.rel),this.z.selectorsMouseoverDelay)}else{this.update(el.href,el.rev,el.rel)}}.j18(this,el);el.z36=function(ev){if(!var_J.v.trident){this.blur()}var_j(ev).stop();return false};el.a("click",el.z36);el.p({"outline":"0"}).a(this.z.thumbChange,el.z34);
						if(this.z.thumbChange=="mouseover")
						{
							el.a("mouseout",el.z34)
						}
						if(this.z.preloadSelectorsSmall)
						{
						var _ba=new Image();
						_ba.src=el.rev
						}if(this.z.preloadSelectorsBig)
							{
							var big=new Image();
							big.src=el.href
							}
							this.z53.push(el)
						}
						}
						,this)
						},
						stop:function(_bc){try{this.j17();this.c.j26("mousemove",this.z46Bind);this.c.j26("mouseout",this.z46Bind);if(undefined==_bc){this.x.self.s()}if(this.r){this.r.stop()}this.y=null;this.z28=false;this.z53.each(function(el){el.j26(this.z.thumbChange,el.z34);if(this.z.thumbChange=="mouseover"){el.j26("mouseout",el.z34)}el.z34=null;el.j26("click",el.z36);el.z36=null},this);if(this.z.hotspots!=""&&var_j(this.z.hotspots)){var_j(this.z.hotspots).s();var_j(this.z.hotspots).z30.insertBefore(var_j(this.z.hotspots),var_j(this.z.hotspots).z31);if(this.c.z32){this.c.removeChild(this.c.z32)}}this.q.unload();this.w.unload();this.r=null;if(this.o){this.c.removeChild(this.o)}if(undefined==_bc){this.c.removeChild(this.x.self);this.e.self.parentNode.removeChild(this.e.self);this.x=null;this.e=null;this.w=null;this.q=null}if(this.z20){clearTimeout(this.z20);this.z20=null}this.z48=null;this.c.z32=null;this.o=null;if(this.c.title==""){this.c.title=this.c.z51}this.z25=-1}catch(e){}},start:function(_be){if(this.z25!=-1){return}this.construct(false,_be)},update:function(big,_c0,_c1){if(var_J.now()-this.z25<300||this.z25==-1){var tm=300-var_J.now()+this.z25;if(this.z25==-1){tm=300}this.z35=setTimeout(this.update.bind(this,big,_c0,_c1),tm);return}this.stop(true);if(undefined!=big){this.c.href=big}if(undefined!=_c0){this.c.firstChild.src=_c0}if(undefined==_c1){_c1=""}if(this.z.preservePosition){_c1="x: "+this.z.x+"; y: "+this.z.y+"; "+_c1}this.start(_c1)},z37:function(_c3){var i=null;var z=[];var z41=_c3.split(";");z41.each(function(_c7){MagicZoom.z40.each(function(el){i=el.exec(_c7.j19());if(i){switch(var_J.j1(MagicZoom.defaults[i[1].k()])){case"boolean":z[i[1].k()]=i[4]==="true";break;case"number":z[i[1].k()]=parseFloat(i[4]);break;default:z[i[1].k()]=i[4]}}},this)},this);if(z.dragMode&&undefined===z.alwaysShowZoom){z.alwaysShowZoom=true}this.z=var_J.extend(this.z,z)},z23:function(){if(!this.x){this.x={self:var_j(document.createElement("DIV")).j2("MagicZoomPup").p({"zIndex":10,"position":"absolute","overflow":"hidden"}).s(),width:20,height:20};this.c.appendChild(this.x.self)}this.x.z39=false;var r=this.e.z44.j7();this.x.height=(this.z.zoomHeight-r.height)/(this.w.height/this.q.height);this.x.width=this.z.zoomWidth/(this.w.width/this.q.width);if(this.x.width>this.q.width){this.x.width=this.q.width}if(this.x.height>this.q.height){this.x.height=this.q.height}this.x.width=Math.round(this.x.width);this.x.height=Math.round(this.x.height);this.x.borderWidth=this.x.self.j30("borderLeftWidth").j22();this.x.self.p({"width":(this.x.width-2*(var_J.v.backCompat?0:this.x.borderWidth))+"px","height":(this.x.height-2*(var_J.v.backCompat?0:this.x.borderWidth))+"px"});if(!this.z.opacityReverse){this.x.self.g(parseFloat(this.z.opacity/100));if(this.x.z45){this.x.self.removeChild(this.x.z45);this.x.z45=null}}else{this.x.self.g(1);if(this.x.z45){this.x.z45.src=this.q.self.src}else{var img=new Image;img.src=this.q.self.src;img.unselectable="on";this.x.z45=var_j(this.x.self.appendChild(img)).p({"position":"absolute","zIndex":5})}}},z46:function(e,r1){if(!this.z28||e===undefined){return false}var_j(e).stop();if(r1===undefined){var r1=var_j(e).j15()}if(this.y==null){this.y=this.q.getBox()}if(r1.x>this.y.right||r1.x<this.y.left||r1.y>this.y.bottom||r1.y<this.y.top){this.j17();return false}if(e.type=="mouseout"){return false}if(this.z.dragMode&&!this.z49){return false}if(!this.z.moveOnClick){r1.x-=this.ddx;r1.y-=this.ddy}if((r1.x+this.x.width/2)>=this.y.right){r1.x=this.y.right-this.x.width/2}if((r1.x-this.x.width/2)<=this.y.left){r1.x=this.y.left+this.x.width/2}if((r1.y+this.x.height/2)>=this.y.bottom){r1.y=this.y.bottom-this.x.height/2}if((r1.y-this.x.height/2)<=this.y.top){r1.y=this.y.top+this.x.height/2}this.z.x=r1.x-this.y.left;this.z.y=r1.y-this.y.top;if(this.z48==null){if(var_J.v.trident){this.c.style.zIndex=1}this.z48=setTimeout(this.z9,10)}return true},j27:function(){var pw=this.x.width/2;var ph=this.x.height/2;this.x.self.style.left=this.z.x-pw+this.q.border.left+"px";this.x.self.style.top=this.z.y-ph+this.q.border.top+"px";if(this.z.opacityReverse){this.x.z45.style.left="-"+(parseFloat(this.x.self.style.left)+this.x.borderWidth)+"px";this.x.z45.style.top="-"+(parseFloat(this.x.self.style.top)+this.x.borderWidth)+"px"}var _cf=(this.z.x-pw)*(this.w.width/this.q.width);var _d0=(this.z.y-ph)*(this.w.height/this.q.height);if(this.w.width-_cf<this.z.zoomWidth){_cf=this.w.width-this.z.zoomWidth}if(this.w.height-_d0<this.z.zoomHeight){_d0=this.w.height-this.z.zoomHeight}if(document.documentElement.dir=="rtl"){_cf=(this.z.x+this.x.width/2-this.q.width)*(this.w.width/this.q.width)}_cf=Math.round(_cf);_d0=Math.round(_d0);if(this.z.smoothing==false||!this.x.z39){this.w.self.style.left=(-_cf)+"px";this.w.self.style.top=(-_d0)+"px"}else{var _d1=parseInt(this.w.self.style.left);var _d2=parseInt(this.w.self.style.top);var dX=(-_cf-_d1);var dY=(-_d0-_d2);if(!dX&&!dY){this.z48=null;return}dX*=this.z.smoothingSpeed/100;if(dX<1&&dX>0){dX=1}else{if(dX>-1&&dX<0){dX=-1}}_d1+=dX;dY*=this.z.smoothingSpeed/100;if(dY<1&&dY>0){dY=1}else{if(dY>-1&&dY<0){dY=-1}}_d2+=dY;this.w.self.style.left=_d1+"px";this.w.self.style.top=_d2+"px"}if(!this.x.z39){if(this.r){this.r.stop();this.r.z.onComplete=var_J.var_F;this.r.z.duration=this.z.zoomFadeInSpeed;this.e.self.g(0);this.r.start({"opacity":[0,1]})}if(this.z.zoomPosition!="inner"){this.x.self.j27()}this.e.self.style.top=this.e.z17;if(this.z.opacityReverse){this.q.self.g(parseFloat((100-this.z.opacity)/100))}this.x.z39=true}if(this.z48){this.z48=setTimeout(this.z9,1000/this.z.fps)}},j17:function(){if(this.z48){clearTimeout(this.z48);this.z48=null}if(!this.z.alwaysShowZoom&&this.x.z39){this.x.z39=false;this.x.self.s();if(this.r){this.r.stop();this.r.z.onComplete=this.e.z18;this.r.z.duration=this.z.zoomFadeOutSpeed;var _d5=this.e.self.j30("opacity");this.r.start({"opacity":[_d5,0]})}else{this.e.s()}if(this.z.opacityReverse){this.q.self.g(1)}}this.y=null;if(this.z.clickToActivate){this.z28=false}if(this.z.dragMode){this.z49=false}if(var_J.v.trident){this.c.style.zIndex=0}},mousedown:function(e){var_j(e).stop();if(this.z.clickToInitialize&&!this.q){this.initMouseEvent=e;this.z11();return}if(this.w&&this.z.clickToActivate&&!this.z28){this.z28=true;this.z46(e)}if(this.z.dragMode){this.z49=true;if(!this.z.moveOnClick){var r1=e.j15();this.ddx=r1.x-this.z.x-this.y.left;this.ddy=r1.y-this.z.y-this.y.top;if(Math.abs(this.ddx)>this.x.width/2||Math.abs(this.ddy)>this.x.height/2){this.z49=false;return}}}if(this.z.moveOnClick){this.z46(e)}},mouseup:function(e){var_j(e).stop();if(this.z.dragMode){this.z49=false}}};
						
if(var_J.v.trident){
	try{
		document.execCommand("BackgroundImageCache",false,true)
	}catch(e)
	{}
}

var_j(document).a("domready",MagicZoom.refresh);
var_j(document).a("mousemove",MagicZoom.z1);

function showPreview(img_path){
	jQuery('#bigimg_src').attr('src', img_path);
	jQuery('#zoom').attr('href', img_path);
	var_j(document).a('domready', MagicZoom.refresh);
	var_j(document).a('mousemove', MagicZoom.z1);
}