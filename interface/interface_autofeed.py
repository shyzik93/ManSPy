import json
import os

file_name_origin = 'autofeed_origin.txt'
file_name_guess = 'autofeed_results.txt'
file_name_sentences = 'autofeed_sentences.txt'

class Interface:

    def __init__(self, api, settings, config):
        self.API = api
        self.settings = settings(read_text=self.read_text)

    def read_text(self, r_text, any_data):
        if self.settings2['compare_with_origin']:
            if self.sentence in self.origin:
                if r_text in self.origin[self.sentence]: self.res.write('    True >>> '+r_text+'\n')
                else:
                    gen_res = False
                    self.res.write('    False >>> '+r_text+'\n')
                    self.res.write('        ORIGINS: '+str(self.origin[self.sentence])+'\n')
            else: self.res.write('    sentence is absent >>> '+r_text+'\n')
        elif self.settings2['write_origin']: self.origin[self.sentence].append(r_text)

    def init(self, settings=None):
        if not settings:
            settings = {'write_origin': False, 'compare_with_origin': True}
        if not os.path.exists(file_name_origin):
            settings = {'write_origin': True, 'compare_with_origin': False}
        #if not settings: settings = {'write_origin': False, 'compare_with_origin': True}
        file_auto = os.path.join(os.path.dirname(__file__), file_name_sentences)
        if not os.path.exists(file_auto):
            f = open(file_auto, 'w')
            f.close()

        if settings['compare_with_origin']:
            f = open(file_name_origin, 'r')
            origin = json.load(f)
            f.close()
            self.res = open(file_name_guess, 'w')
        elif settings['write_origin']:
            origin = {}

        gen_res = True
        with open(file_auto, 'r') as file_sentences:
            t = 0 #time.time()
            for sentence in file_sentences:
                sentence = sentence.strip()
                if not sentence or sentence[0] == '#': continue
                if settings['compare_with_origin']: self.res.write(sentence+'\n')
                if settings['write_origin']:
                    origin[sentence] = []

                self.sentence = sentence
                self.settings2 = settings
                self.origin = origin

                msg, res = self.API.write_text(sentence, self.settings)
                #msg = self.API.write_text(self, sentence)
                t += msg.time_total


            #t = time.time() - t
            print('\n---- All sentences: ', t)

        if settings['compare_with_origin']:
            self.res.write(str(gen_res)+'\n')
            self.res.close()
        elif settings['write_origin']:
            f = open(file_name_origin, 'w')
            f.write(json.dumps(origin))
            f.close()
