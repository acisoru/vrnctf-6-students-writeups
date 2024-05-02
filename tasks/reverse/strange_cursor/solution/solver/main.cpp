#include <Windows.h>

void setMySuperHook() {
	HINSTANCE hLib = LoadLibraryA("user32.dll");

	if (!hLib)
		return;

	FARPROC hookedAddress = GetProcAddress(hLib, "SetCursorPos");

	if (!hookedAddress)
		return;

	/*Тут вставляются байты, которые были представлены в диалоге задачи*/
	CHAR patch[5] = { 0x0000FFFFFFFF, 0x000000000025, 0x000000000004, 0x0000FFFFFF9C, 0x000000000030 };

	WriteProcessMemory(GetCurrentProcess(), (LPVOID)hookedAddress, patch, 5, NULL);
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD dwReasonForCall, LPVOID lpReserved) {
	if (dwReasonForCall == DLL_PROCESS_ATTACH) 
		setMySuperHook();

	return TRUE;
}