"""تركيب الإعلان الجديد. يعمل محلياً أو على GitHub Actions: python3 build.py  (يخرج promo_v2.mp4)"""
import subprocess,sys
V="scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p"
SC=[("ibn_al_qayyim","W1"),("ibn_taymiyyah","W2"),("ibn_khaldun","W4"),("ibn_sina","W3")]
cmd=["ffmpeg","-loglevel","error","-y","-i","in/s1.mp4","-i","in/s2.mp4","-i","in/app_capture.mp4","-i","in/s6.mp4","-loop","1","-t","5.5","-i","in/end_card.png"]   # 0..4
for s,b in SC: cmd+=["-loop","1","-t","2.5","-i",f"in/{b}_m.jpg","-stream_loop","-1","-t","2.5","-i",f"in/hero_{s}_idle.mp4"]   # 5..12
OV=[("h",0.4,2.6),("n1",5.2,2.1),("n2",7.7,2.1),("n3",10.2,2.1),("n4",12.7,2.1),("cap",5.0,10.0)]
for k,_,_ in OV: cmd+=["-loop","1","-t","30","-i",f"{k}.png"]   # 13..18
f=[f"[0:v]trim=0:3,setpts=PTS-STARTPTS,{V}[c0]",f"[1:v]trim=2:4,setpts=PTS-STARTPTS,{V}[c1]"]
for i in range(4):
    b,h=5+2*i,6+2*i
    f.append(f"[{b}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=rgba[bg{i}]")
    f.append(f"[{h}:v]split[a{i}][m{i}];[a{i}]crop=560:880:0:0,format=rgba[col{i}];[m{i}]crop=560:880:0:880,format=gray[mat{i}];[col{i}][mat{i}]alphamerge,scale=-1:1300,format=rgba[fig{i}]")
    f.append(f"[bg{i}][fig{i}]overlay=(W-w)/2:H-h-170:format=auto:shortest=1,trim=0:2.5,setpts=PTS-STARTPTS,{V}[sc{i}]")
f.append(f"[2:v]setpts=1.2*PTS,tpad=stop_mode=clone:stop_duration=0.5,trim=0:4.5,setpts=PTS-STARTPTS,{V}[c2]")
f.append(f"[3:v]trim=2:5,setpts=PTS-STARTPTS,{V}[c3]")
f.append(f"[4:v]trim=0:5.5,setpts=PTS-STARTPTS,{V}[c4]")
f.append("[c0][c1][sc0][sc1][sc2][sc3][c2][c3][c4]concat=n=9:v=1:a=0[base]")
last="base"
for j,(k,st,d) in enumerate(OV):
    f.append(f"[{13+j}:v]format=rgba,trim=0:{d},setpts=PTS-STARTPTS,fade=in:st=0:d=0.35:alpha=1,fade=out:st={d-0.35}:d=0.35:alpha=1,setpts=PTS+{st}/TB[o{j}]")
    f.append(f"[{last}][o{j}]overlay=eof_action=pass[l{j}]"); last=f"l{j}"
f.append(f"[{last}]fade=t=in:d=0.3,fade=t=out:st=27.6:d=0.4[vout]")
cmd+=["-filter_complex",";".join(f),"-map","[vout]","-t","28","-c:v","libx264","-crf","18","-preset","veryfast","-pix_fmt","yuv420p","-an","v2_only.mp4"]
r=subprocess.run(cmd,capture_output=True,text=True);print("V",r.stderr[-1200:],flush=True)
# audio
vo=[("va",0.2),("vb",5.2),("vc",15.3),("vd",22.7)]
ac=["ffmpeg","-loglevel","error","-y"]
for k,_ in vo: ac+=["-i",k+".mp3"]
ac+=["-f","lavfi","-t","28","-i","anoisesrc=color=brown:amplitude=0.5:sample_rate=44100","-f","lavfi","-t","28","-i","anoisesrc=color=pink:amplitude=0.5:sample_rate=44100"]
af=[f"[{i}:a]aresample=44100,adelay={int(t*1000)}|{int(t*1000)}[v{i}]" for i,(k,t) in enumerate(vo)]
af.append("[4:a]lowpass=f=400,volume=0.05[room]")
af.append("[5:a]lowpass=f=1800,highpass=f=600,volume='0.25*(lt(abs(t-3.4),0.04)+lt(abs(t-3.9),0.04)+lt(abs(t-4.5),0.04))':eval=frame[tap]")
af.append("[v0][v1][v2][v3][room][tap]amix=inputs=6:normalize=0,alimiter=limit=0.9,afade=t=in:d=0.3,afade=t=out:st=27:d=1[aud]")
ac+=["-filter_complex",";".join(af),"-map","[aud]","-t","28","-c:a","aac","-b:a","192k","a2.m4a"]
print("A",subprocess.run(ac,capture_output=True,text=True).stderr[-600:],flush=True)
print(subprocess.run(["ffmpeg","-loglevel","error","-y","-i","v2_only.mp4","-i","a2.m4a","-c","copy","-shortest","promo_v2.mp4"],capture_output=True,text=True).stderr)
