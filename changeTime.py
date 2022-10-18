import pefile,time,pywintypes,os,sys
from win32con import FILE_FLAG_BACKUP_SEMANTICS
from win32con import FILE_SHARE_WRITE
from win32file import CloseHandle
from win32file import CreateFile
from win32file import GENERIC_WRITE
from win32file import OPEN_EXISTING
from win32file import SetFileTime

def modifyFileTime(path, fakeTime):
	try:
		format_str = "%Y-%m-%d %H:%M:%S"
		pe = pefile.PE(path)
		st = time.strptime(fakeTime, format_str)
		cmpTime = int(time.mktime(st))
		pe.FILE_HEADER.TimeDateStamp = cmpTime
		pe.write(path + ".qigpig")
		print("compilationTime: " + str(time.strftime(format_str, time.localtime(pe.FILE_HEADER.TimeDateStamp))))
		pe.close()
		os.remove(path)
		os.rename(path + ".qigpig", path)
		filehandle = CreateFile(path, GENERIC_WRITE, FILE_SHARE_WRITE, None, OPEN_EXISTING,FILE_FLAG_BACKUP_SEMANTICS, 0)
		changeTime = pywintypes.Time(time.mktime(time.strptime(fakeTime, format_str)))
		SetFileTime(filehandle, changeTime, changeTime, changeTime)
		CloseHandle(filehandle)
		print('createTime: {}'.format(changeTime))
		print('updateTime: {}'.format(changeTime))
		print('accessTime: {}'.format(changeTime))
	except Exception as e:
		print(e)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		filename = sys.argv[1]
		if os.path.exists(filename):
			modifyFileTime(filename, "2020-01-21 15:12:29")
		else:
			print("path does not exist")
	else:
		print("useage: python3 changeTime.py filename")