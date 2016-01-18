/**Program:本程序基于团车网Android客户端 v2.40版
 * Author:Chen Changlei
 * 
 */
package com.mingrisoft.test;
import com.robotium.solo.*;
import android.test.ActivityInstrumentationTestCase2;

@SuppressWarnings("rawtypes")
public class Login_Logout extends ActivityInstrumentationTestCase2 {
  	private Solo solo;
  	
  	private static final String LAUNCHER_ACTIVITY_FULL_CLASSNAME = "com.tuanche.app.activity.StartActivity";

    private static Class<?> launcherActivityClass;
    static{
        try {
            launcherActivityClass = Class.forName(LAUNCHER_ACTIVITY_FULL_CLASSNAME);
        } catch (ClassNotFoundException e) {
           throw new RuntimeException(e);
        }
    }
  	
  	@SuppressWarnings("unchecked")
    public Login_Logout() throws ClassNotFoundException {
        super(launcherActivityClass);
    }
  	/**
  	 * 初始化
  	 */
  	public void setUp() throws Exception {
        super.setUp();
		solo = new Solo(getInstrumentation(), getActivity());
		
  	}
  	/**
  	 * 
  	 * 团车登录
  	 */
	public void testLogin() throws Exception{
		System.out.println("开始执行测试");
		solo.waitForActivity("StartActivity", 2000);//激活程序入口 'com.tuanche.app.activity.StartActivity'
		solo.takeScreenshot();//屏幕截图
 		assertTrue("MainActivity is not found!", solo.waitForActivity("MainActivity"));//主菜单入口'com.tuanche.app.activity.MainActivity'
		solo.clickOnText(java.util.regex.Pattern.quote("我的"));//点击 我的
		solo.clickOnView(solo.getView("bt_login"));//点击 马上登录
		assertTrue("LoginActivity is not found!", solo.waitForActivity("LoginActivity"));//登录入口'com.tuanche.app.activity.LoginActivity'
		solo.clickOnView(solo.getView("tv_common_login"));//点击 账号登录
		solo.clickOnView(solo.getView("username"));//点击用户名文本框
		solo.clearEditText((android.widget.EditText) solo.getView("username"));  //清理用户名文本框内容
		solo.enterText((android.widget.EditText) solo.getView("username"), "15369652510");//输入用户名
		solo.clickOnView(solo.getView("password")); //点击密码文本框
		solo.clearEditText((android.widget.EditText) solo.getView("password"));//清空密码文本框内容
		solo.enterText((android.widget.EditText) solo.getView("password"), "111111");//输入密码
		solo.clickOnView(solo.getView("login_btn")); //点击登录
    	assertTrue("MainActivity is not found!", solo.waitForActivity("MainActivity"));
    	solo.sleep(500);
	}
	/**
	 * 
	 * 底价购车、询价
	 */
	public void testMction() throws Exception{
		assertTrue("MainActivity is not found!", solo.waitForActivity("MainActivity"));
		solo.clickOnText(java.util.regex.Pattern.quote("首页"));
		solo.clickOnView(solo.getView("backTV")); //点击左上角定位
		solo.clickOnView(solo.getView("column_title"));//点击北京
		solo.clickOnText("底价购车");
//		solo.clickOnView(solo.getView("bottom_special_name"));
		solo.clickOnText("大众");
		solo.clickOnText("捷达");
		solo.clickOnText("1.6L 手动时尚型");
		solo.clickOnView(solo.getView("tv_car_color"));
		solo.clickOnText("糖果白");
		solo.clickOnView(solo.getView("tv_buy_plan"));
		solo.clickOnText("短期内暂无购车计划");
		solo.clickOnView(solo.getView("tv_buy_or_exchange"));
		solo.clickOnText("新车全款");
		solo.clickOnView(solo.getView("tv_take_car_city"));
		solo.clickOnText("北京");
		solo.clickOnView(solo.getView("tv_registration_city"));
		solo.clickOnText("北京");
		solo.clickOnView(solo.getView("btn_ask_price"));
		solo.clickOnView(solo.getView("backIV"));
		solo.sleep(500);
	}
	/**
	 * 
	 * 电商购车报名
	 */
	public void testModify() throws Exception{
//		assertTrue("MainActivity is not found!", solo.waitForActivity("MainActivity"));
		solo.clickOnText(java.util.regex.Pattern.quote("首页"));
		solo.clickOnView(solo.getView("backFL"));
		solo.clickOnText("滕州");
		solo.clickOnView(solo.getView("inputTitleTV"));//点击搜索框
		solo.clickOnView(solo.getView("searchContentEditText"));//点击搜索框
//		solo.clearEditText((android.widget.EditText) solo.getView("searchContentEditText"));  //清理文本框内容
		solo.enterText((android.widget.EditText) solo.getView("searchContentEditText"), "奥迪A3");//输入查询内容
		solo.clickOnView(solo.getView("searchButton")); //点击查询按钮
//		solo.clickOnText("奥迪A3");
		solo.clickOnView(solo.getView("styleNameTV"));
		solo.clickOnView(solo.getView("et_input_name"));
		solo.clearEditText((android.widget.EditText) solo.getView("et_input_name"));
		solo.enterText((android.widget.EditText) solo.getView("et_input_name"), "tuanche");
		solo.clickOnView(solo.getView("et_input_phone"));
		solo.clearEditText((android.widget.EditText) solo.getView("et_input_phone"));
		solo.enterText((android.widget.EditText) solo.getView("et_input_phone"), "15369652511");
		solo.clickOnButton("团购报名");
		solo.clickOnView(solo.getView("tv_car_color"));
		solo.clickOnText("Sportback 35 TFSI 手动进取型");
		solo.clickOnView(solo.getView("tv_buy_plan"));
		solo.clickOnText("不确定");
		solo.clickOnView(solo.getView("tv_buy_or_exchange"));
		solo.clickOnText("否");
		solo.clickOnView(solo.getView("tv_other_requirement_label"));
		solo.enterText((android.widget.EditText) solo.getView("tv_other_requirement_label"), "10000");
		solo.clickOnButton("立即报名");
		solo.sleep(500);
	}
	/**
	 * 
	 * 团车退出登录
	 */
	public void testNLogout() throws Exception{
		assertTrue("MainActivity is not found!", solo.waitForActivity("MainActivity"));
		solo.clickOnText(java.util.regex.Pattern.quote("我的"));//点击 我的
//		assertTrue("无法启动用户中心类", solo.waitForActivity("UserCenterActivity", 30000));
		solo.clickOnView(solo.getView("tv_name"));
		solo.clickOnView(solo.getView("commit"));//点击退出登录
		solo.clickOnView(solo.getView("dialog_commit"));//点击确认，退出登录
	}
	/**
	 * 测试完毕，回收资源
	 */
   	@Override
   	public void tearDown() throws Exception {
        solo.finishOpenedActivities();
//        super.tearDown();
  	}
}

