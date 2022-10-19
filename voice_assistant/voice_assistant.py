import rclpy
import subprocess
from rclpy.node import Node
from std_msgs.msg import String
import threading

from gtts import gTTS
from playsound import playsound

class VoiceAssistant(Node):
    def __init__(self):
        super().__init__('voice_assistant')
        open_jtalk = ['open_jtalk']
        mech = ['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
        htsvoice = ['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
        speed = ['-r','1.0']
        outwav = ['-ow','open_jtalk.wav']
        self.jtalk_cmd =  open_jtalk+mech+htsvoice+speed+outwav
        
        self.voice_list = ['ボイスアシスタント、起動しました']

        self.subscription = self.create_subscription(
            String,
            '/voice_assistant',
            self.append_voice,
            10
        )

        self.subscription
    
    def append_voice(self, msg):
        self.voice_list.append(msg.data)
        self.get_logger().info("Voice appended, current size : %d"% len(self.voice_list))

    def listener_callback(self):
        self.get_logger().info("listener callback")
        while len(self.voice_list) > 0:
            voice = self.voice_list.pop(0)
            self.get_logger().info('Voice Assistant %s'% voice)
            self.jtalk(voice)

    def jtalk(self, t):
        c = subprocess.Popen(self.jtalk_cmd, stdin=subprocess.PIPE)
        c.stdin.write(t.encode())
        c.stdin.close()
        c.wait()
        aplay = ['aplay','-q','open_jtalk.wav']
        wr = subprocess.Popen(aplay)


def main(args=None):
    rclpy.init(args=args)

    voice_assistant = VoiceAssistant()
    
    while rclpy.ok():
        voice_assistant.listener_callback()
        rclpy.spin_once(voice_assistant)

    voice_assistant.destroy_node()
    rclpy.shutdown()

if __name__=="__main__":
    main()