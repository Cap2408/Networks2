import java.io.*;

public class CmdTest {
	public static void Nmap_command(String addr, int frequency){
		String command = "cmd /c start cmd.exe /K ";
		String bucket = "\"Nmap -n -sP "+addr+"\"";
		int i = 0;
		int j=2;
		for(;;){
			i = 0;
			for(i=0;i<frequency;i++){			
				try {
					Process p = Runtime.getRuntime().exec(command+bucket+"\" > output\""+(j++)+"\".txt\"");
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				try {
					Thread.sleep(60*60*1000/frequency);
					//	try{Thread.sleep(500);}catch(InterruptedException e){System.out.println(e);}  
				}
				catch(InterruptedException e){System.out.println(e);}

			}
		}	
		
	}
	public static void main(String[] args) throws Exception {
		Nmap_command(args[0],Integer.parseInt(args[1]));
	}
}


		//ProcessBuilder builder = new ProcessBuilder(
		//  "cmd.exe", "/c", "cd \"C:\\Program Files\\Microsoft SQL Server\" && dir");
		//builder.redirectErrorStream(true);
		//Process p = builder.start();
		//BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
		//String line;
		//while (true) {
		//  line = r.readLine();
		//  if (line == null) { break; }
		//  System.out.println(line);
		//}
