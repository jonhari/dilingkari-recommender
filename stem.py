
from nltk.stem.snowball import StemmerI


class IndonesianStemmer(StemmerI):
    """
    The indonesian snowball stemmer
    """    
    
    REMOVED_KE = 1;
    REMOVED_PENG = 2;
    REMOVED_DI = 4;
    REMOVED_MENG = 8;
    REMOVED_TER = 16;
    REMOVED_BER = 32;
    REMOVED_PE = 64;
    
    def __init__(self):
        self.num_syllables = 0
        self.stem_derivational = True
        

    def stem(self, word):
        self.flags = 0
        # number of syllables == number of vowels
        self.num_syllables = len([c for c in word if self._is_vowel(c)])
        self.word = word
        
        if self.num_syllables > 2:
            self._remove_particle()
            
        if self.num_syllables >= 2:
            self._remove_possessive_pronoun()
            
        if self.stem_derivational:
            self._stem_derivational()
        
        return self.word
    
    def _is_vowel(self, letter):
        """
        Vowels in indonesian
        """
        return letter in [u'a', u'e', u'i', u'o', u'u']
    
    def _remove_particle(self):
        """ 
        Remove common indonesian particles, adjust number of syllables 
        """
        suffix = self.word[-3:]
        if suffix in [u'kah', u'lah', u'pun']:
            self.num_syllables -= 1
            self.word = self.word[:-3]
            
    def _remove_possessive_pronoun(self):
        """
        Remove possessive pronoun particles
        """
        if self.word[-2:] in [u'ku', u'mu']:
            self.num_syllables -= 2
            self.word = self.word[:-2]
            return
        
        if self.word[-3:] == u'nya':
            self.num_syllables -= 1
            self.word = self.word[:-3]
            
    def _stem_derivational(self):
        old_length = len(self.word)
        
        if self.num_syllables > 2:
            self._remove_first_order_prefix()
        
        if old_length != len(self.word): # A rule has fired
            old_length = len(self.word)

            if self.num_syllables > 2:
                self._remove_suffix()
                
            if old_length != len(self.word): # A rule has fired
                if self.num_syllables > 2:
                    self._remove_second_order_prefix
                        
        else: # fail
            if self.num_syllables > 2:
                self._remove_second_order_prefix()
                
            if self.num_syllables > 2:
                self._remove_suffix()
                
                
    def _remove_first_order_prefix(self):
        """ Remove FIRST ORDER PREFIX """
        if self.word.startswith(u'meng'):
            self.flags |= IndonesianStemmer.REMOVED_MENG
            self.num_syllables -= 1
            self.word = self.word[4:]
            return
        
        if self.word.startswith(u'meny') and \
           len(self.word) > 4 and self._is_vowel(self.word[4]):
            self.flags |= IndonesianStemmer.REMOVED_MENG
            self.word = self.word[0:3] + u's' + self.word[4:] 
            self.num_syllables -= 1
            self.word = self.word[3:]
            return
        
        if self.word[0:3] in [u'men', u'mem']:
            self.flags |= IndonesianStemmer.REMOVED_MENG
            self.num_syllables -= 1
            self.word = self.word[3:]
            return
        
        if self.word.startswith(u'me'):
            self.flags |= IndonesianStemmer.REMOVED_MENG
            self.num_syllables -= 1
            self.word = self.word[2:]
            return

        if self.word.startswith(u'peng'):
            self.flags |= IndonesianStemmer.REMOVED_PENG
            self.num_syllables -= 1
            self.word = self.word[4:]
            return        

        if self.word.startswith(u'peny') and \
            len(self.word) > 4 and self._is_vowel(self.word[4]):
             self.flags |= IndonesianStemmer.REMOVED_PENG
             #self.word[3] = u's'
             self.word = self.word[0:3] + u's' + self.word[4:]
             self.num_syllables -= 1
             self.word = self.word[3:]
             return        
        
        if self.word.startswith(u'peny'):
            self.flags |= IndonesianStemmer.REMOVED_PENG
            self.num_syllables -= 1
            self.word = self.word[4:]
            return
        
        if self.word.startswith(u'pen') and \
           len(self.word) > 3 and self._is_vowel(self.word[3]):
            self.flags |= IndonesianStemmer.REMOVED_PENG
            #self.word[2] = u't'
            self.word = self.word[0:2] + u't' + self.word[3:]
            self.num_syllables -= 1
            self.word = self.word[2:]
            return
        
        if self.word[0:3] in [u'pen', u'pem']:
            self.flags |= IndonesianStemmer.REMOVED_PENG
            self.num_syllables -= 1
            self.word = self.word[2:]
            return
        
        if self.word.startswith(u'di'):
            self.flags |= IndonesianStemmer.REMOVED_DI
            self.num_syllables -= 1
            self.word = self.word[2:]
            return
        
        if self.word.startswith(u'ter'):
            self.flags |= IndonesianStemmer.REMOVED_TER
            self.num_syllables -= 1
            self.word = self.word[3:]
            return 
        
        if self.word.startswith(u'ke'):
            self.flags |= IndonesianStemmer.REMOVED_KE
            self.num_syllables -= 1
            self.word = self.word[2:]
            return        
        
    def _remove_second_order_prefix(self):
        """ Remove SECOND ORDER PREFIX """
        if self.word.startswith(u'ber'):
            self.flags |= IndonesianStemmer.REMOVED_BER
            self.num_syllables -= 1
            self.word = self.word[3:]
            return
            
        if self.word == u'belajar':
            self.flags |= IndonesianStemmer.REMOVED_BER
            self.num_syllables -= 1
            self.word = self.word[3:]
            return
        
        if self.word.startswith(u'be') and len(self.word) > 4 and \
           not self._is_vowel(self.word[2]) \
           and self.word[3] == u'e' and self.word[4] == 'r':
            self.flags |= IndonesianStemmer.REMOVED_BER
            self.num_syllables -= 1
            self.word = self.word[2:]
            return
        
        if self.word.startswith(u'per'):
            self.num_syllables -= 1
            self.word = self.word[3:]
            return
        
        if self.word == u'pelajar':
            self.num_syllables -= 1
            self.word = self.word[3:]
            return
        
        if self.word.startswith(u'pe'):
            self.flags |= IndonesianStemmer.REMOVED_PE
            self.num_syllables -= 1
            self.word = self.word[2:]
            return
            
    def _remove_suffix(self):
        if self.word.endswith(u'kan') \
           and not self.flags & IndonesianStemmer.REMOVED_KE \
           and not self.flags & IndonesianStemmer.REMOVED_PENG \
           and not self.flags & IndonesianStemmer.REMOVED_PE:
            self.num_syllables -= 1
            self.word = self.word[:-3]
            return
        
        if self.word.endswith(u'an') \
           and not self.flags & IndonesianStemmer.REMOVED_DI \
           and not self.flags & IndonesianStemmer.REMOVED_MENG \
           and not self.flags & IndonesianStemmer.REMOVED_TER:
            self.num_syllables -= 1
            self.word = self.word[:-2]
            return
        
        if self.word.endswith(u'i') \
           and not self.word.endswith(u'si') \
           and not self.flags & IndonesianStemmer.REMOVED_BER \
           and not self.flags & IndonesianStemmer.REMOVED_KE \
           and not self.flags & IndonesianStemmer.REMOVED_PENG:
            self.num_syllables -= 1
            self.word = self.word[:-1]
            return
    
    def stop_words(self):
        """return list of Indonesian stop words"""
        
        return ['tiba-tiba',
                 'kepada',
                 'mengapa',
                 'haruslah',
                 'secukupnya',
                 'sekaligus',
                 'tiba',
                 'per',
                 'kata',
                 'kesampaian',
                 'sedikitnya',
                 'sejak',
                 'kamulah',
                 'dikarenakan',
                 'to',
                 'setibanya',
                 'setempat',
                 'ialah',
                 'turut',
                 'sekali-kali',
                 'seluruh',
                 'utama',
                 'sesaat',
                 'hendaklah',
                 'ingin',
                 'depan',
                 'sebanyak',
                 'siapa',
                 'lain',
                 'tersebut',
                 'diketahui',
                 'dimisalkan',
                 'meminta',
                 'sekurang-kurangnya',
                 'kapanpun',
                 'amatlah',
                 'semakin',
                 'selamanya',
                 'dia',
                 'seseorang',
                 'bagaimana',
                 'gunakan',
                 'sana',
                 'sebagainya',
                 'menyangkut',
                 'makanya',
                 'karenanya',
                 'umum',
                 'bung',
                 'diberi',
                 'biasanya',
                 'saya',
                 'sedangkan',
                 'pentingnya',
                 'disebutkan',
                 'bersama-sama',
                 'dapat',
                 'usah',
                 'tambahnya',
                 'masing-masing',
                 'dituturkan',
                 'merekalah',
                 'semata-mata',
                 'berikan',
                 'minta',
                 'kitalah',
                 'keduanya',
                 'guna',
                 'lewat',
                 'tanya',
                 'dengan',
                 'apakah',
                 'jangan',
                 'berkehendak',
                 'bermacam-macam',
                 'bilakah',
                 'bagaikan',
                 'didatangkan',
                 'hingga',
                 'bertutur',
                 'memberi',
                 'kami',
                 'mula',
                 'dibuatnya',
                 'keluar',
                 'dikira',
                 'ditegaskan',
                 'kamu',
                 'sini',
                 'perlunya',
                 'pukul',
                 'sedemikian',
                 'berdatangan',
                 'sajalah',
                 'sesudah',
                 'kelihatannya',
                 'seolah',
                 'aku',
                 'telah',
                 'mengetahui',
                 'dimulai',
                 'tersebutlah',
                 'disinilah',
                 'sekaranglah',
                 'dimulainya',
                 'keinginan',
                 'sekalipun',
                 'menegaskan',
                 'menyatakan',
                 'tambah',
                 'menyampaikan',
                 'enak',
                 'masuk',
                 'berlainan',
                 'sebut',
                 'dimaksudnya',
                 'pihak',
                 'sesuatu',
                 'apa',
                 'misalnya',
                 'menanti-nanti',
                 'tanyanya',
                 'mempertanyakan',
                 'anda',
                 'dipergunakan',
                 'next',
                 'walau',
                 'jelas',
                 'sesekali',
                 'adalah',
                 'terjadilah',
                 'diungkapkan',
                 'akankah',
                 'hendak',
                 'ditunjuknya',
                 'antaranya',
                 'datang',
                 'kalaulah',
                 'sepertinya',
                 'malah',
                 'kemungkinan',
                 'inikah',
                 'menginginkan',
                 'berjumlah',
                 'berlangsung',
                 'pastilah',
                 'seingat',
                 'setiba',
                 'seberapa',
                 'bersama',
                 'nyata',
                 'cukupkah',
                 'sekecil',
                 'lihat',
                 'mempersiapkan',
                 'ibu',
                 'oleh',
                 'memisalkan',
                 'siapapun',
                 'selaku',
                 'katakanlah',
                 'sama-sama',
                 'penting',
                 'memintakan',
                 'bertanya',
                 'mungkin',
                 'menyeluruh',
                 'diibaratkannya',
                 'sebagian',
                 'tak',
                 'tandasnya',
                 'lama',
                 'kecil',
                 'belum',
                 'berikut',
                 'lanjutnya',
                 'justru',
                 'kadar',
                 'sekiranya',
                 'selalu',
                 'padanya',
                 'semisalnya',
                 'maksud',
                 'mengatakannya',
                 'entahlah',
                 'lah',
                 'sekadar',
                 'mereka',
                 'sebenarnya',
                 'dirinya',
                 'benar',
                 'bekerja',
                 'bagaimanakah',
                 'menunjuk',
                 'sebagaimana',
                 'berada',
                 'atau',
                 'berbagai',
                 'sebisanya',
                 'memastikan',
                 'ataupun',
                 'pertanyaan',
                 'sedikit',
                 'sinilah',
                 'berawal',
                 'manakala',
                 'paticle',
                 'se',
                 'ikut',
                 'banyak',
                 'nanti',
                 'waduh',
                 'orang',
                 'meski',
                 'dijelaskannya',
                 'menyebutkan',
                 'beginian',
                 'itu',
                 'teringat-ingat',
                 'sendirinya',
                 'caranya',
                 'menghendaki',
                 'dilakukan',
                 'adanya',
                 'sebesar',
                 'masihkah',
                 'tandas',
                 'enggaknya',
                 'empat',
                 'memperkirakan',
                 'yakni',
                 'terdahulu',
                 'artinya',
                 'diibaratkan',
                 'antara',
                 'dan',
                 'terdapat',
                 'ditanyakan',
                 'seolah-olah',
                 'terutama',
                 'lanjut',
                 'pertanyakan',
                 'sambil',
                 'mendapat',
                 'pak',
                 'kiranya',
                 'menanyai',
                 'tempat',
                 'cukup',
                 'untuk',
                 'inilah',
                 'waktu',
                 'kamilah',
                 'terhadapnya',
                 'sudahkah',
                 'semaunya',
                 'didapat',
                 'tentu',
                 'begitupun',
                 'tampaknya',
                 'dong',
                 'hari',
                 'soalnya',
                 'mengibaratkannya',
                 'terus',
                 'menurut',
                 'cuma',
                 'menggunakan',
                 'jelasnya',
                 'segera',
                 'malahan',
                 'mau',
                 'bermacam',
                 'diingat',
                 'seperti',
                 'kira-kira',
                 'semisal',
                 'ibaratkan',
                 'tanyakan',
                 'belakangan',
                 'selama-lamanya',
                 'mata',
                 'sangatlah',
                 'sampai',
                 'bagian',
                 'ternyata',
                 'semasa',
                 'pun',
                 'setidaknya',
                 'langsung',
                 'awalnya',
                 'seluruhnya',
                 'termasuk',
                 'tiap',
                 'diperlukannya',
                 'buat',
                 'berikutnya',
                 'tahun',
                 'diri',
                 'cara',
                 'entah',
                 'mampukah',
                 'tentulah',
                 'mendatang',
                 'kenapa',
                 'nantinya',
                 'kalaupun',
                 'tahu',
                 'secara',
                 'ditandaskan',
                 'kalian',
                 'pertama',
                 'benarkah',
                 'punya',
                 'segala',
                 'dini',
                 'katanya',
                 'sebutlah',
                 'beginikah',
                 'saatnya',
                 'dibuat',
                 'kapan',
                 'terkira',
                 'lamanya',
                 'memerlukan',
                 'bahwasanya',
                 'kok',
                 'atas',
                 'semuanya',
                 'siap',
                 'harus',
                 'toh',
                 'kerja',
                 'bukannya',
                 'juga',
                 'setiap',
                 'keterlaluan',
                 'seketika',
                 'diperlihatkan',
                 'akan',
                 'para',
                 'mengibaratkan',
                 'sangkut',
                 'meyakini',
                 'ditunjukkannya',
                 'berupa',
                 'mempersoalkan',
                 'dilalui',
                 'tersampaikan',
                 'sesudahnya',
                 'bisakah',
                 'hanya',
                 'melihatnya',
                 'enggak',
                 'apalagi',
                 'kini',
                 'mengucapkannya',
                 'menanyakan',
                 'bahkan',
                 'begini',
                 'melalui',
                 'sekitar',
                 'diakhirinya',
                 'seringnya',
                 'rata',
                 'menunjukkan',
                 'setengah',
                 'pro',
                 'naik',
                 'membuat',
                 'sejauh',
                 'sekadarnya',
                 'dipersoalkan',
                 'mengatakan',
                 'macam',
                 'soal',
                 'mulailah',
                 'maupun',
                 'dipunyai',
                 'bolehkah',
                 'inginkan',
                 'ataukah',
                 'sela',
                 'inginkah',
                 'diingatkan',
                 'tentunya',
                 'itukah',
                 'semata',
                 'sering',
                 'mendapatkan',
                 'menanya',
                 'tepat',
                 'menunjuknya',
                 'menuturkan',
                 'sendiri',
                 'kan',
                 'kebetulan',
                 'amat',
                 'jangankan',
                 'tegas',
                 'tinggi',
                 'dahulu',
                 'ke',
                 'dijelaskan',
                 'bulan',
                 'yang',
                 'terdiri',
                 'lagian',
                 'ketika',
                 'kita',
                 'sesuatunya',
                 'sekurangnya',
                 'itulah',
                 'tegasnya',
                 'kembali',
                 'kemudian',
                 'memberikan',
                 'baik',
                 'akhir',
                 'keadaan',
                 'bahwa',
                 'rasa',
                 'menambahkan',
                 'belumlah',
                 'boleh',
                 'berakhirlah',
                 'perlu',
                 'tunjuk',
                 'tapi',
                 'berturut',
                 'menjadi',
                 'ibarat',
                 'dituturkannya',
                 'mulai',
                 'berapalah',
                 'melakukan',
                 'di',
                 'terjadi',
                 'berapakah',
                 'jumlahnya',
                 'olehnya',
                 'sebab',
                 'diberikannya',
                 'sebelum',
                 'diminta',
                 'sebaik-baiknya',
                 'percuma',
                 'numeral',
                 'dipertanyakan',
                 'khususnya',
                 'tengah',
                 'sebuah',
                 'memperbuat',
                 'ditunjuki',
                 'tampak',
                 'sejumlah',
                 'diantara',
                 'dipastikan',
                 'menjelaskan',
                 'lalu',
                 'hampir',
                 'pada',
                 'sempat',
                 'baru',
                 'tertentu',
                 'jadi',
                 'bagai',
                 'menunjuki',
                 'manalagi',
                 'sebagai',
                 'mengingatkan',
                 'diperbuatnya',
                 'katakan',
                 'menjawab',
                 'karena',
                 'dimungkinkan',
                 'bagainamakah',
                 'suatu',
                 'begitu',
                 'dikerjakan',
                 'memungkinkan',
                 'mungkinkah',
                 'sebaik',
                 'rupa',
                 'keseluruhannya',
                 'dimaksudkannya',
                 'sedang',
                 'berarti',
                 'awal',
                 'sehingga',
                 'tuju',
                 'sepantasnyalah',
                 'seharusnya',
                 'bagaimanapun',
                 'diperkirakan',
                 'terlihat',
                 'cukuplah',
                 'tidakkah',
                 'misalkan',
                 'begitulah',
                 'dilihat',
                 'biasa',
                 'tetapi',
                 'akhiri',
                 'berapa',
                 'menaiki',
                 'memang',
                 'mana',
                 'masalahnya',
                 'ungkap',
                 'tutur',
                 'terlebih',
                 'memihak',
                 'dimaksud',
                 'disampaikan',
                 'sekitarnya',
                 'ujar',
                 'makin',
                 'berlalu',
                 'bahwasannya',
                 'semula',
                 'meyakinkan',
                 'berakhirnya',
                 'sendirian',
                 'dua',
                 'daripada',
                 'sebetulnya',
                 'ditujukan',
                 'hendaknya',
                 'menuju',
                 'menantikan',
                 'antar',
                 'diantaranya',
                 'bermula',
                 'ibaratnya',
                 'bermaksud',
                 'rasanya',
                 'tiga',
                 'setidak-tidaknya',
                 'lebih',
                 'tanpa',
                 'kinilah',
                 'demikianlah',
                 'persoalan',
                 'terjadinya',
                 'bila',
                 'agak',
                 'semampu',
                 'agar',
                 'sesama',
                 'bawah',
                 'benarlah',
                 'rupanya',
                 'diperlukan',
                 'bakalan',
                 'terhadap',
                 'berujar',
                 'demi',
                 'kasus',
                 'semampunya',
                 'seusai',
                 'ia',
                 'disini',
                 'pihaknya',
                 'kapankah',
                 'saling',
                 'kedua',
                 'sekali',
                 'balik',
                 'sama',
                 'diperbuat',
                 'maka',
                 'diberikan',
                 'mempunyai',
                 'diucapkan',
                 'belakang',
                 'sampaikan',
                 'betulkah',
                 'bagi',
                 'ingat',
                 'sepantasnya',
                 'ditambahkan',
                 'semacam',
                 'yakin',
                 'merasa',
                 'mendatangkan',
                 'ingat-ingat',
                 'dimaksudkan',
                 'nyatanya',
                 'memulai',
                 'disebut',
                 'umumnya',
                 'tertuju',
                 'merupakan',
                 'sebaliknya',
                 'hanyalah',
                 'dari',
                 'mempergunakan',
                 'adjectice',
                 'kelihatan',
                 'ujarnya',
                 'namun',
                 'sesampai',
                 'jawab',
                 'terakhir',
                 'nyaris',
                 'kala',
                 'terlalu',
                 'sangat',
                 'kali',
                 'ucap',
                 'tadinya',
                 'jauh',
                 'setelah',
                 'selain',
                 'sekalian',
                 'mengungkapkan',
                 'sebutnya',
                 'hal',
                 'teringat',
                 'demikian',
                 'akhirnya',
                 'perlukah',
                 'agaknya',
                 'ada',
                 'andalah',
                 'adapun',
                 'laku',
                 'jumlah',
                 'jikalau',
                 'pernah',
                 'tuturnya',
                 'sebelumnya',
                 'panjang',
                 'siapakah',
                 'mengira',
                 'sekarang',
                 'mengenai',
                 'ungkapnya',
                 'bukanlah',
                 'masih',
                 'janganlah',
                 'kelima',
                 'melihat',
                 'kira',
                 'mendatangi',
                 'jadinya',
                 'bertanya-tanya',
                 'bukan',
                 'jika',
                 'continue',
                 'sebaiknya',
                 'mirip',
                 'sebegini',
                 'page',
                 'berkali-kali',
                 'sesegera',
                 'tetap',
                 'melainkan',
                 'pertama-tama',
                 'supaya',
                 'segalanya',
                 'masing',
                 'sudahlah',
                 'sebabnya',
                 'apabila',
                 'semua',
                 'menanti',
                 'dekat',
                 'lima',
                 'sejenak',
                 'jawabnya',
                 'ditanya',
                 'saat',
                 'sudah',
                 'walaupun',
                 'sementara',
                 'jelaslah',
                 'mampu',
                 'ditanyai',
                 'terasa',
                 'usai',
                 'lainnya',
                 'mengucapkan',
                 'padahal',
                 'pasti',
                 'wong',
                 'kelamaan',
                 'asal',
                 'tidak',
                 'luar',
                 'dimintai',
                 'sampai-sampai',
                 'beberapa',
                 'menyiapkan',
                 'kurang',
                 'digunakan',
                 'jelaskan',
                 'begitukah',
                 'bakal',
                 'dikatakan',
                 'jawaban',
                 'bisa',
                 'yaitu',
                 'sebegitu',
                 'wahai',
                 'seperlunya',
                 'masalah',
                 'tadi',
                 'kemungkinannya',
                 'besar',
                 'disebutkannya',
                 'menandaskan',
                 'tidaklah',
                 'wah',
                 'dalam',
                 'jadilah',
                 'lagi',
                 'bolehlah',
                 'berakhir',
                 'memperlihatkan',
                 'berapapun',
                 'dulu',
                 'diketahuinya',
                 'berkata',
                 'akulah',
                 'ditunjuk',
                 'arti',
                 'berturut-turut',
                 'beri',
                 'saja',
                 'mengingat',
                 'masa',
                 'satu',
                 'pula',
                 'bersiap-siap',
                 'bukankah',
                 'mengakhiri',
                 'tentang',
                 'kalau',
                 'sewaktu',
                 'seorang',
                 'semasih',
                 'kepadanya',
                 'mengerjakan',
                 'paling',
                 'pantas',
                 'diinginkan',
                 'ditunjukkan',
                 'ini',
                 'dialah',
                 'dimulailah',
                 'seenaknya',
                 'berkeinginan',
                 'diakhiri',
                 'keseluruhan',
                 'selanjutnya',
                 'serupa',
                 'nah',
                 'setinggi',
                 'meskipun',
                 'betul',
                 'berkenaan',
                 'bersiap',
                 'seterusnya',
                 'mulanya',
                 'dikatakannya',
                 'harusnya',
                 'waktunya',
                 'bapak',
                 'dijawab',
                 'diucapkannya',
                 'apaan',
                 'apatah',
                 'kena',
                 'serta',
                 'beginilah',
                 'khusus',
                 'terbanyak',
                 'asalkan',
                 'sayalah',
                 'selama',
                 'sepanjang',
                 'sepihak',
                 'hadap',
                 'ucapnya',
                 'misal',
                 'berlebihan']

if __name__ == "__main__":
    stemmer = IndonesianStemmer()
    assert stemmer.stem(u'diakah') == u'dia'
    assert stemmer.stem(u'sayalah') == u'saya'
    assert stemmer.stem(u'tasmu') == u'tas'
    assert stemmer.stem(u'sepedaku') == u'sepeda'
    assert stemmer.stem(u'berlari') == u'lari'
    assert stemmer.stem(u'dimakan') == u'makan'
    assert stemmer.stem(u'kekasih') == u'kasih'
    assert stemmer.stem(u'mengambil') == u'ambil'
    assert stemmer.stem(u'pengatur') == u'atur'
    assert stemmer.stem(u'perlebar') == u'lebar'
    assert stemmer.stem(u'terbaca') == u'baca'
    assert stemmer.stem(u'gulai') == u'gula'
    assert stemmer.stem(u'makanan') == u'makan'
    assert stemmer.stem(u'permainan') == u'main'
    assert stemmer.stem(u'kemenangan') == u'menang'
    assert stemmer.stem(u'berjatuhan') == u'jatuh'
    assert stemmer.stem(u'mengambili') == u'ambil'