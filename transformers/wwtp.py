# Transform WWTP fasta headers to fastq dito
# Fredrik Boulund 2016

def transform_fasta_header(fastaheader):
    """
    Do some string operations on FASTA headers to make them look like FASTQ
    headers.

    FASTA headers look like:
      >102B_1_HISEQ_138_D2DGEACXX_6_1101_6736_39162_1_N_0_ATTACTCGTAATCTTA 
    FASTQ headers look like:
      @HISEQ:138:D2DGEACXX:7:1101:1231:2207 2:N:0:TCCGGAGAGTACTGAC
    FASTQ filenames look like:
      8_130829_BD2DGEACXX_P477_235B_dual32_1_val_1.fq
    """
    fastq_source, read = fastaheader.split(" ", 1)[0].split("_HISEQ")
    read_header = read.split("_")
    read_header = "HISEQ:"+":".join(read_header[1:6])+" "+":".join(read_header[6:])
    fastq_base = fastq_source.rsplit("_", 1)[0]
    return fastq_base, read_header

def fastq_filename(fastq_base):
    """
    Return a pair of complete fastq filenames for fastq_base.
    """
    return fastq_filenames[fastq_base]+"1.fq", fastq_filenames[fastq_base]+"2.fq",


fastq_filenames = {
"103":  "1_130829_BD2DGEACXX_P477_103_dual3_1_val_",   
"104":  "1_130829_BD2DGEACXX_P477_104_dual4_1_val_",   
"112":  "1_130829_BD2DGEACXX_P477_112_dual12_1_val_",  
"129B": "1_130829_BD2DGEACXX_P477_129B_dual29_1_val_", 
"137B": "1_130829_BD2DGEACXX_P477_137B_dual37_1_val_", 
"146":  "1_131008_AC2G2AACXX_P477_146_index5_1_val_",  
"147":  "1_131008_AC2G2AACXX_P477_147_index7_1_val_",  
"148":  "1_131008_AC2G2AACXX_P477_148_index8_1_val_",  
"149":  "1_131008_AC2G2AACXX_P477_149_index9_1_val_",  
"150":  "1_131008_AC2G2AACXX_P477_150_index10_1_val_", 
"105":  "2_130829_BD2DGEACXX_P477_105_dual5_1_val_",   
"106":  "2_130829_BD2DGEACXX_P477_106_dual6_1_val_",   
"113":  "2_130829_BD2DGEACXX_P477_113_dual13_1_val_",  
"114":  "2_130829_BD2DGEACXX_P477_114_dual14_1_val_",  
"121":  "2_130829_BD2DGEACXX_P477_121_dual21_1_val_",  
"151":  "2_131008_AC2G2AACXX_P477_151_index11_1_val_", 
"152":  "2_131008_AC2G2AACXX_P477_152_index12_1_val_", 
"153":  "2_131008_AC2G2AACXX_P477_153_index13_1_val_", 
"154":  "2_131008_AC2G2AACXX_P477_154_index14_1_val_", 
"155":  "2_131008_AC2G2AACXX_P477_155_index15_1_val_", 
"107":  "3_130829_BD2DGEACXX_P477_107_dual7_1_val_",   
"108":  "3_130829_BD2DGEACXX_P477_108_dual8_1_val_",   
"115":  "3_130829_BD2DGEACXX_P477_115_dual15_1_val_",  
"123":  "3_130829_BD2DGEACXX_P477_123_dual23_1_val_",  
"216":  "3_130829_BD2DGEACXX_P477_216_dual16_1_val_",  
"156":  "3_131008_AC2G2AACXX_P477_156_index16_1_val_", 
"157":  "3_131008_AC2G2AACXX_P477_157_index17_1_val_", 
"158":  "3_131008_AC2G2AACXX_P477_158_index18_1_val_", 
"159":  "3_131008_AC2G2AACXX_P477_159_index19_1_val_", 
"160":  "3_131008_AC2G2AACXX_P477_160_index20_1_val_", 
"122":  "4_130829_BD2DGEACXX_P477_122_dual22_1_val_",  
"130":  "4_130829_BD2DGEACXX_P477_130_dual30_1_val_",  
"138":  "4_130829_BD2DGEACXX_P477_138_dual38_1_val_",  
"228":  "4_130829_BD2DGEACXX_P477_228_dual28_1_val_",  
"236":  "4_130829_BD2DGEACXX_P477_236_dual36_1_val_",  
"161":  "4_131008_AC2G2AACXX_P477_161_index21_1_val_", 
"162":  "4_131008_AC2G2AACXX_P477_162_index22_1_val_", 
"163":  "4_131008_AC2G2AACXX_P477_163_index23_1_val_", 
"164":  "4_131008_AC2G2AACXX_P477_164_index24_1_val_", 
"165":  "4_131008_AC2G2AACXX_P477_165_index1_1_val_",  
"124":  "5_130829_BD2DGEACXX_P477_124_dual24_1_val_",  
"131":  "5_130829_BD2DGEACXX_P477_131_dual31_1_val_",  
"139":  "5_130829_BD2DGEACXX_P477_139_dual39_1_val_",  
"140":  "5_130829_BD2DGEACXX_P477_140_dual40_1_val_",  
"232F": "5_130829_BD2DGEACXX_P477_232F_dual32_1_val_", 
"166":  "5_131008_AC2G2AACXX_P477_166_index2_1_val_",  
"167":  "5_131008_AC2G2AACXX_P477_167_index3_1_val_",  
"168":  "5_131008_AC2G2AACXX_P477_168_index4_1_val_",  
"169":  "5_131008_AC2G2AACXX_P477_169_index5_1_val_",  
"170":  "5_131008_AC2G2AACXX_P477_170_index6_1_val_",  
"102B": "6_130829_BD2DGEACXX_P477_102B_dual6_1_val_",  
"111B": "6_130829_BD2DGEACXX_P477_111B_dual13_1_val_", 
"117FB": "6_130829_BD2DGEACXX_P477_117FB_dual14_1_val_",
"201B": "6_130829_BD2DGEACXX_P477_201B_dual5_1_val_",  
"220B": "6_130829_BD2DGEACXX_P477_220B_dual21_1_val_", 
"109B": "7_130829_BD2DGEACXX_P477_109B_dual7_1_val_",  
"110B": "7_130829_BD2DGEACXX_P477_110B_dual8_1_val_",  
"118FB": "7_130829_BD2DGEACXX_P477_118FB_dual15_1_val_",
"119FB": "7_130829_BD2DGEACXX_P477_119FB_dual16_1_val_",
"226B": "7_130829_BD2DGEACXX_P477_226B_dual23_1_val_", 
"225B": "8_130829_BD2DGEACXX_P477_225B_dual22_1_val_", 
"227B": "8_130829_BD2DGEACXX_P477_227B_dual24_1_val_", 
"233B": "8_130829_BD2DGEACXX_P477_233B_dual30_1_val_", 
"234B": "8_130829_BD2DGEACXX_P477_234B_dual31_1_val_", 
"235B": "8_130829_BD2DGEACXX_P477_235B_dual32_1_val_", 
"141":  "8_131002_BC2G8KACXX_P477_141_index1_1_val_",  
"142":  "8_131002_BC2G8KACXX_P477_142_index2_1_val_",  
"143":  "8_131002_BC2G8KACXX_P477_143_index3_1_val_",  
"144":  "8_131002_BC2G8KACXX_P477_144_index4_1_val_",  
"145":  "8_131002_BC2G8KACXX_P477_145_index5_1_val_",  
}
