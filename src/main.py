import ctypes
import ctypes.wintypes



def struct(nm,rfl,**f):
	def _d_wr(self):
		o={}
		for k in self._fields_:
			o[k[0]]=self.__getattribute__(k[0])
		return o
	ncls=type(nm,(ctypes.Structure,),{"dict":_d_wr,"_fields_":[(k,v) for k,v in f.items()]})
	ptr=ctypes.POINTER(ncls)
	for rf in rfl:
		rf.restype=ptr
	return ncls



ERR_CODES={0x00000000:"FTLIB_ERR_SUCCESS",0xE0000100:"FTLIB_ERR_NO_MEMORY",0xE0001000:"FTLIB_ERR_FAILED",0xE000100C:"FTLIB_ERR_TIMEOUT",0xE0001018:"FTLIB_ERR_INVALID_PARAM",0xE0001101:"FTLIB_ERR_SOME_DEVICES_ARE_OPEN",0xE0001102:"FTLIB_ERR_DEVICE_IS_OPEN",0xE0001103:"FTLIB_ERR_DEVICE_NOT_OPEN",0xE0001104:"FTLIB_ERR_NO_SUCH_DEVICE_INSTANCE",0xE0001283:"FTLIB_ERR_UNKNOWN_DEVICE_HANDLE",0xE0001286:"FTLIB_ERR_LIB_IS_INITIALIZED",0xE0001287:"FTLIB_ERR_LIB_IS_NOT_INITIALIZED",0xE00012A0:"FTLIB_ERR_THREAD_NOT_STARTABLE",0xE00012A5:"FTLIB_ERR_THREAD_IS_RUNNING",0xE00012A6:"FTLIB_ERR_THREAD_NOT_RUNNING",0xE00012AF:"FTLIB_ERR_THREAD_SYNCHRONIZED",0xE00012B0:"FTLIB_ERR_TIMEOUT_TA",0xE00012B1:"FTLIB_ERR_CREATE_EVENT",0xE00012B2:"FTLIB_ERR_CREATE_MM_TIMER",0xE0001400:"FTLIB_ERR_UPLOAD_FILE_NOT_OPEN",0xE0001401:"FTLIB_ERR_UPLOAD_FILE_READ_ERR",0xE0001402:"FTLIB_ERR_UPLOAD_INVALID_FSIZE",0xE0001403:"FTLIB_ERR_UPLOAD_START",0xE0001404:"FTLIB_ERR_UPLOAD_CANCELED",0xE0001405:"FTLIB_ERR_UPLOAD_FAILED",0xE0001406:"FTLIB_ERR_UPLOAD_TIMEOUT",0xE0001407:"FTLIB_ERR_UPLOAD_ACK",0xE0001408:"FTLIB_ERR_UPLOAD_NAK",0xE0001409:"FTLIB_ERR_UPLOAD_DONE",0xE000140A:"FTLIB_ERR_UPLOAD_FLASHWRITE",0xE000140B:"FTLIB_ERR_REM_CMD_FAILED",0xE000140C:"FTLIB_ERR_REM_CMD_NOT_SUPPORTED",0xE000140D:"FTLIB_ERR_FWUPD_GET_FILES",0xE000140E:"FTLIB_ERR_FWUPD_NO_FILES",0xE0001905:"FTLIB_ERR_ACCESS_DENIED",0xE0001906:"FTLIB_ERR_OPEN_COM",0xE0001908:"FTLIB_ERR_INIT_COM",0xE0001909:"FTLIB_ERR_INIT_COM_TIMEOUT",0xE0002000:"FTLIB_ERR_WRONG_HOSTNAME_LEN",0xE0003000:"FTLIB_FWUPD_UPLOAD_START",0xE0003001:"FTLIB_FWUPD_UPLOAD_DONE",0xE0003002:"FTLIB_FWUPD_TIMEOUT",0xE0003003:"FTLIB_FWUPD_FLUSH_DISK",0xE0003004:"FTLIB_FWUPD_CLEAN_DISK",0xE0003005:"FTLIB_FWUPD_ERR_FILE_READ",0xE0003006:"FTLIB_FWUPD_UPLOAD_FAILED",0xE0003007:"FTLIB_FWUPD_STARTING",0xE0003008:"FTLIB_FWUPD_FINISHED",0xE0003009:"FTLIB_FWUPD_REM_COMMAND",0xE000300A:"FTLIB_FWUPD_REM_TIMEOUT",0xE000300B:"FTLIB_FWUPD_REM_FAILED",0xE000300C:"FTLIB_FWUPD_IZ_STEPS",0xE000300D:"FTLIB_FWUPD_STEP",0xE0004000:"FTLIB_BT_INVALID_CONIDX",0xE0004001:"FTLIB_BT_CON_NOT_EXISTS",0xE0004002:"FTLIB_BT_CON_ACTIVE",0xE0004003:"FTLIB_BT_CON_INACTIVE",0xE0004004:"FTLIB_BT_CON_WRONG_ADDR",0xE0004005:"FTLIB_BT_CON_WAIT_BUSY",0xE0005000:"FTLIB_I2C_INVALID_DEV_ADDR",0xE0005001:"FTLIB_I2C_C_INVALID_FLAGS_ADDRMODE",0xE0005002:"FTLIB_I2C_C_INVALID_FLAGS_DATAMODE",0xE0005003:"FTLIB_I2C_C_INVALID_FLAGS_ERRMODE",0xEFFFFFFF:"FTLIB_ERR_UNKNOWN"}
MOTOR_1=COUNTER_1=0
MOTOR_2=COUNTER_2=1
MOTOR_3=COUNTER_3=2
MOTOR_4=COUNTER_4=3
OUTPUT_PIN_1=INPUT_1=0
OUTPUT_PIN_2=INPUT_2=1
OUTPUT_PIN_3=INPUT_3=2
OUTPUT_PIN_4=INPUT_4=3
OUTPUT_PIN_5=INPUT_5=4
OUTPUT_PIN_6=INPUT_6=5
OUTPUT_PIN_7=INPUT_7=6
OUTPUT_PIN_8=INPUT_8=7
MOTOR_ON=SINGLE_OFF=True
MOTOR_OFF=SINLE_ON=False
MIN_OUTPUT_VALUE=0
MAX_OUTPUT_VALUE=512
COUNTER_NORMAL=0
COUNTER_INVERTED=1
RAM_DISK=0
FLASH_DISK=1
SYSTEM_DISK=1
FT_LIB_DLL=ctypes.WinDLL("./ftMscLibEx.dll")
TA_STATUS=struct("TA_STATUS",[FT_LIB_DLL.GetTransferAreaStatusAddr],status=ctypes.c_uint8,iostatus=ctypes.c_uint8,ComErr=ctypes.c_uint16)



def get_error(err):
	err_s=ctypes.create_string_buffer(128)
	FT_LIB_DLL.ftxGetLibErrorString(ctypes.wintypes.DWORD(err),ctypes.wintypes.DWORD(1),err_s,ctypes.wintypes.DWORD(128))
	return [err&0xffffffff,ERR_CODES[err&0xffffffff],str(err_s.value,"utf-8")]



class FtLib:
	@staticmethod
	def version():
		s=ctypes.create_string_buffer(128)
		FT_LIB_DLL.ftxGetLibVersionStr(s,ctypes.wintypes.DWORD(128))
		return str(s.value,"utf-8")



	@staticmethod
	def init():
		return get_error(FT_LIB_DLL.ftxInitLib())



	@staticmethod
	def is_init():
		return get_error(FT_LIB_DLL.ftxIsLibInit())



	@staticmethod
	def open_device(port,baud_rate=9600):
		dw=ctypes.wintypes.DWORD()
		if (type(port)==int):
			h=FT_LIB_DLL.ftxOpenComDeviceNr(ctypes.wintypes.DWORD(port),ctypes.wintypes.DWORD(baud_rate),ctypes.byref(dw))
			if (dw.value!=0):
				return get_error(dw.value)
			return FtDevice("COM"+str(port),h)
		else:
			h=FT_LIB_DLL.ftxOpenComDevice(ctypes.c_char_p(bytes(port,"utf-8")),ctypes.wintypes.DWORD(baud_rate),ctypes.byref(dw))
			if (dw.value!=0):
				return get_error(dw.value)
			return FtDevice(port,h)



	@staticmethod
	def get_avaible_com_ports(usb_only=False):
		n=FT_LIB_DLL.GetAvailableComPorts((0 if usb_only==False else 1))
		o=[]
		for i in range(0,n):
			s=ctypes.create_string_buffer(128)
			e=FT_LIB_DLL.EnumComPorts(ctypes.wintypes.DWORD(i),s,ctypes.wintypes.DWORD(128));
			if (e!=0):
				return get_error(e)
			o+=[str(s.value,"utf-8")]
		return o



	@staticmethod
	def close():
		e=FT_LIB_DLL.ftxCloseAllDevices()
		if (e!=0):
			return get_error(e)
		return get_error(FT_LIB_DLL.ftxInitLib())



class FtDevice:
	def __init__(self,p,h):
		self.port=p
		self._h=h
		self._ta_ptr=-1



	def __repr__(self):
		return f"FtDevice(port={self.port}, handle={hex(self._h)})"



	def frimware_version(self):
		s=ctypes.create_string_buffer(128)
		FT_LIB_DLL.GetRoboTxFwStr(self._h,0,s,ctypes.wintypes.DWORD(128))
		return str(s.value,"utf-8")



	def hardware_version(self):
		s=ctypes.create_string_buffer(128)
		FT_LIB_DLL.GetRoboTxHwStr(self._h,0,s,ctypes.wintypes.DWORD(128))
		return str(s.value,"utf-8")



	def dll_version(self):
		s=ctypes.create_string_buffer(128)
		FT_LIB_DLL.GetRoboTxDllStr(self._h,0,s,ctypes.wintypes.DWORD(128))
		return str(s.value,"utf-8")



	def serial_number(self):
		s=ctypes.create_string_buffer(128)
		FT_LIB_DLL.GetRoboTxSerialStr(self._h,0,s,ctypes.wintypes.DWORD(128))
		return str(s.value,"utf-8")



	def name(self,name=None):
		if (name is None):
			s=ctypes.create_string_buffer(128)
			FT_LIB_DLL.GetRoboTxDevName(self._h,0,s,ctypes.wintypes.DWORD(128))
			return str(s.value,"utf-8")
		else:
			return get_error(FT_LIB_DLL.SetRoboTxDevName(self._h,0,ctypes.c_char_p(bytes(name[:16],"utf-8"))))



	def bluetooth_address(self):
		s=ctypes.create_string_buffer(128)
		FT_LIB_DLL.GetRoboTxBtAddr(self._h,0,s,ctypes.wintypes.DWORD(128))
		return str(s.value,"utf-8")



	def start_io(self):
		e=FT_LIB_DLL.ftxStartTransferArea(self._h)
		if (e==0):
			return FtDeviceIO(self._h)
		return get_error(e);



	def io_active(self):
		return get_error(FT_LIB_DLL.ftxIsTransferActiv(self._h))



	def clear_disk(self,disk_id):
		return get_error(FT_LIB_DLL.RTxCleanDisk(self._h,ctypes.wintypes.DWORD(disk_id)))



	def set_message(self,msg):
		return get_error(FT_LIB_DLL.SetRoboTxMessage(self._h,0,ctypes.create_string_buffer(bytes(msg[:98],"utf-8"))))



	def upload_file(self,fp,nm):
		self._ret=None
		slf=self
		def of(v):
			slf._ret=v
		with open(fp,"rb") as f:
			dt=f.read()
		v=ctypes.c_char_p(dt)
		e=FT_LIB_DLL.FtRamFileUpload(self._h,0,ctypes.cast(v,ctypes.c_void_p),len(dt),ctypes.c_char_p(bytes(nm,"utf-8")),ctypes.CFUNCTYPE(None,ctypes.wintypes.DWORD)(of))
		if (e!=0):
			return get_error(e)
		while (self._ret!=True):
			print(self._ret)
		return self._ret



	def run_command(self,cmd):
		self._ret=None
		slf=self
		def f(v,_):
			slf._ret=str(v,"utf-8")
		e=FT_LIB_DLL.FtRemoteCmd(self._h,ctypes.create_string_buffer(bytes(cmd,"utf-8")),ctypes.CFUNCTYPE(None,ctypes.c_char_p,ctypes.wintypes.DWORD)(f))
		if (e!=0):
			return get_error(e)
		while (self._ret is None):
			pass
		return self._ret



	def close(self):
		return get_error(FT_LIB_DLL.ftxCloseDevice(self._h))



class FtDeviceIO:
	def __init__(self,h):
		self._h=h
		self._m={0:True,1:True,2:True,3:True}
		for i in range(0,4):
			FT_LIB_DLL.SetFtMotorConfig(self._h,0,i,True)
			FT_LIB_DLL.SetOutMotorValues(self._h,0,i,0,0)



	def status(self):
		return FT_LIB_DLL.GetTransferAreaStatusAddr(self._h,0).contents.dict()



	def reset_counter(self,cnt_id):
		return get_error(FT_LIB_DLL.StartCounterReset(self._h,0,cnt_id))



	def set_counter_state(self,cnt_id,mode):
		return get_error(FT_LIB_DLL.SetFtCntConfig(self._h,0,cnt_id,mode))



	def get_counter(self,cnt_id):
		v=ctypes.c_int16()
		st=ctypes.c_int16()
		FT_LIB_DLL.GetInCounterValue.argtypes=(ctypes.wintypes.HANDLE,ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_int16),ctypes.POINTER(ctypes.c_int16))
		e=FT_LIB_DLL.GetInCounterValue(self._h,0,cnt_id,v,st)
		if (e!=0):
			return get_error(e)
		return [v.value,st.value]



	def set_output_mode(self,o_id,mode):
		if (self._m[o_id]==mode):
			return None
		self._m[o_id]=mode
		e=FT_LIB_DLL.SetFtMotorConfig(self._h,0,o_id,mode)
		if (e!=0):
			return get_error(e)
		if (mode==True):
			FT_LIB_DLL.SetOutMotorValues(self._h,0,o_id,0,0)
		else:
			FT_LIB_DLL.SetOutPwmValues(self._h,0,o_id*2,0)
			FT_LIB_DLL.SetOutPwmValues(self._h,0,o_id*2+1,0)
		return None



	def start_motor(self,m_id,a,b):
		self.set_output_mode(m_id,True)
		return get_error(FT_LIB_DLL.SetOutMotorValues(self._h,0,m_id,a,b))



	def stop_motor(self,m_id):
		return get_error(FT_LIB_DLL.StopMotorExCmd(self._h,0,m_id))



	def stop_all_motors(self):
		return get_error(FT_LIB_DLL.StopAllMotorExCmd(self._h,0))



	def set_output(self,p_id,v):
		self.set_output_mode(p_id//2,False)
		return get_error(FT_LIB_DLL.SetOutPwmValues(self._h,0,p_id,v))



	def get_input(self,i_id):
		v=ctypes.c_int16()
		ov_r=ctypes.c_uint32()
		FT_LIB_DLL.GetInIOValue.argtypes=(ctypes.wintypes.HANDLE,ctypes.c_int,ctypes.c_int,ctypes.POINTER(ctypes.c_int16),ctypes.POINTER(ctypes.c_uint32))
		e=FT_LIB_DLL.GetInIOValue(self._h,0,i_id,v,ov_r)
		if (e!=0):
			return get_error(e)
		return [v.value,ov_r.value]



	def get_buttons(self):
		l=ctypes.c_int16()
		r=ctypes.c_int16()
		FT_LIB_DLL.GetInDisplayButtonValue.argtypes=(ctypes.wintypes.HANDLE,ctypes.c_int,ctypes.POINTER(ctypes.c_int16),ctypes.POINTER(ctypes.c_int16))
		e=FT_LIB_DLL.GetInDisplayButtonValue(self._h,0,l,r)
		if (e!=0):
			return get_error(e)
		return [l.value,r.value]



	def close(self):
		return get_error(FT_LIB_DLL.ftxStopTransferArea(self._h))



FtLib.version()
FtLib.init()
FtLib.is_init()
FtLib.get_avaible_com_ports()
d=FtLib.open_device("COM3")
d.frimware_version()
d.hardware_version()
d.dll_version()
d.serial_number()
d.name()
d.name("Krzem5")
d.bluetooth_address()
io=d.start_io()
d.io_active()
io.status()
io.reset_counter(COUNTER_1)
io.set_counter_state(COUNTER_1,COUNTER_INVERTED)
import time
e=time.time()+5
while (time.time()<=e):
	print(io.get_counter(COUNTER_1))
	time.sleep(0.025)
io.start_motor(MOTOR_1,MIN_OUTPUT_VALUE,MAX_OUTPUT_VALUE)
time.sleep(0.25)
io.stop_motor(MOTOR_1)
time.sleep(0.25)
io.set_output(OUTPUT_PIN_1,MAX_OUTPUT_VALUE)
time.sleep(0.5)
io.stop_all_motors()
e=time.time()+5
while (time.time()<=e):
	print(io.get_input(INPUT_1))
	time.sleep(0.025)
e=time.time()+5
while (time.time()<=e):
	print(io.get_buttons())
	time.sleep(0.025)
print(d.run_command("dir ramdisk"))
d.clear_disk(FLASH_DISK)
print(d.set_message("This is a Message!"))
time.sleep(0.1)
d.upload_file("./file.txt","Ufile.txt")
d.run_program()
d.stop_program()
io.close()
d.close()
FtLib.close()
