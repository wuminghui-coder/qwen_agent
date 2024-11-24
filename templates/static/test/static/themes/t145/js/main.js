/*
Powered by ly200.com		http://www.ly200.com
广州联雅网络科技有限公司		020-83226791
*/
$(function ($){
	showthis('.description .hd span','.description .bd >div',0,'cur');
	$('.description .hd span').click(function(){
		showthis('.description .hd span','.description .bd .desc_txt',$(this).index(),'cur');
	});
	nav(".nav .warp",".nav .i");
	$('#tabv .item').click(function(){
		$('#tabv .item').eq($(this).index()).addClass('cur').siblings('#tabv .item').removeClass('cur');
		$('.tab').eq($(this).index()).show().siblings('.tab').hide();	
	});	
	
	//首页新闻
	function index_news(){
		var nlist = $('.home_news .box .nlist');
		var list = $('.list', nlist);
		var one = $('.one', list);
		var iW = one.width();
		list.width(iW*one.length);
		var speed = 300;
		if (one.length>1){
			var leftbtn = $('.home_news .box .title .cbtn span').eq(0);//左按钮
			var rightbtn = $('.home_news .box .title .cbtn span').eq(1);//右按钮
			leftbtn.on('click', function (){
				list.prepend(function () {
					$(this).css('margin-left', -iW);
					return $('.one', this).last();
				}).stop(true, true).animate({'margin-left':0}, speed);
			});
			rightbtn.on('click', function (){
				list.stop(true, true).animate({'margin-left':-iW}, speed, function (){
					list.css('margin-left', function (){
						$('.one', this).eq(0).appendTo(list);
						return 0;
					})
				});
			});
		}
	}
	index_news();
	$(window).resize(function (){index_news()});
	//侧栏
	$('.leftmenu .y .n1').on('click', function (){
		$(this).parent('.y').toggleClass('on');
	});
	$('.leftmenu .y .n1 a').on('click', function (e){
		e.stopPropagation();
	});
	
	//产品小图
	var simg = $('.pro_detail .img .s_img');
	var simg_list = $('.list', simg);
	var simg_item = $('.i', simg_list);
	if (simg_item.length>4){
		simg_list.width(simg_item.length*simg_item.eq(0).outerWidth(true));
		small_pic_move(simg, simg_list, 40, 1);
	}
});

function small_pic_move(box, list, spaceW, type){//spaceW 移入多少范围开始执行
	var tips = 0;//左，上1 右，下2 其他0
	var Tid = '';
	var speed = 60;
	
	if (type==1){
		var boxW = box.width();
		var listW = list.outerWidth(true);
		var property = 'margin-left';
	}else{
		var boxW = box.height();
		var listW = $(list).outerHeight(true);
		var property = 'margin-top';
	}
	var xy = 0;
	box.mousemove(function(e) {
		xy = type==1 ? (e.pageX-$(this).offset().left) : (e.pageY-$(this).offset().top);
		if (xy<spaceW){//左边
			if (tips!=1){
				tips = 1;
				Tid = setInterval(function (){
					if (parseInt(list.css(property))<0){
						list.css(property, '+=2');
					}else{
						clearInterval(Tid);
					}
				}, speed);
			}
		}else if (xy>boxW-spaceW){//右边
			if (tips!=2){
				tips = 2;
				Tid = setInterval(function (){
					if (parseInt(list.css(property))>boxW-listW){
						list.css(property, '-=2');
					}else{
						clearInterval(Tid);
					}
				}, speed);
			}
		}else{
			if (tips!=0){
				tips = 0;
				clearInterval(Tid);
			}
		}
	});
	box.mouseleave(function (){
		clearInterval(Tid);
		tips = 0;
	});
}
