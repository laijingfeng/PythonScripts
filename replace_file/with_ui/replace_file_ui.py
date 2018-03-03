# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MainFrameUI
###########################################################################

class MainFrameUI ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 320,330 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"目录", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.m_text_dir = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.m_text_dir.SetToolTipString( u"把目录拖拽到这里" )
		
		bSizer2.Add( self.m_text_dir, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, 0, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"规则", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_textCtrl_rule = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,100 ), wx.TE_MULTILINE )
		self.m_textCtrl_rule.SetToolTipString( u"[xxx]-[yyy]" )
		
		bSizer3.Add( self.m_textCtrl_rule, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		self.m_checkBox_recursion = wx.CheckBox( self, wx.ID_ANY, u"是否递归处理", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_checkBox_recursion, 0, wx.ALL, 5 )
		
		self.m_checkBox_with_name = wx.CheckBox( self, wx.ID_ANY, u"处理文件名称", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_checkBox_with_name, 0, wx.ALL, 5 )
		
		self.m_checkBox_with_content = wx.CheckBox( self, wx.ID_ANY, u"处理文件内容", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer1.Add( self.m_checkBox_with_content, 0, wx.ALL, 5 )
		
		self.m_button_replace = wx.Button( self, wx.ID_ANY, u"替换", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		bSizer1.Add( self.m_button_replace, 0, wx.ALL, 5 )
		
		self.m_textCtrl_tip = wx.TextCtrl( self, wx.ID_ANY, u"提示：拖拽目录到输入框", wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.m_textCtrl_tip.Enable( False )
		
		bSizer1.Add( self.m_textCtrl_tip, 0, wx.ALL, 5 )
		
		
		self.SetSizer( bSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button_replace.Bind( wx.EVT_BUTTON, self.onClickReplace )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def onClickReplace( self, event ):
		event.Skip()
	

