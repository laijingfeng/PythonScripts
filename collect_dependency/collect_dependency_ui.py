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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"收集依赖", pos = wx.DefaultPosition, size = wx.Size( 320,255 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"查找目录", wx.DefaultPosition, wx.Size( -1,-1 ), 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.m_textCtrl_dir = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.m_textCtrl_dir.SetToolTipString( u"把目录拖拽到这里" )
		
		bSizer2.Add( self.m_textCtrl_dir, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer2, 1, 0, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"存放目录", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer3.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.m_textCtrl_save = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.m_textCtrl_save.SetToolTipString( u"把目录拖拽到这里" )
		
		bSizer3.Add( self.m_textCtrl_save, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		bSizer31 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"配置文件", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		bSizer31.Add( self.m_staticText31, 0, wx.ALL, 5 )
		
		self.m_textCtrl_json = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		self.m_textCtrl_json.SetToolTipString( u"把文件拖拽到这里，xxx.json" )
		
		bSizer31.Add( self.m_textCtrl_json, 0, wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer31, 1, wx.EXPAND, 5 )
		
		self.m_checkBox_clean = wx.CheckBox( self, wx.ID_ANY, u"是否先清空目录", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_clean.SetToolTipString( u"是否先清空目录" )
		
		bSizer1.Add( self.m_checkBox_clean, 0, wx.ALL, 5 )
		
		self.m_button_replace = wx.Button( self, wx.ID_ANY, u"查找", wx.Point( -1,-1 ), wx.DefaultSize, 0 )
		bSizer1.Add( self.m_button_replace, 0, wx.ALL, 5 )
		
		self.m_textCtrl_tip = wx.TextCtrl( self, wx.ID_ANY, u"提示：正常", wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
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
	

