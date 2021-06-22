# --------------------------------------------------------------------------- #
# Description: GGPLOT
#
# Contains all ggplot scripts that are automated.
# Put in here only functions that are tested and run smoothly.
#
# --------------------------------------------------------------------------- #


# --------------------------------------------------------------------------- #
# GGPLOT
# --------------------------------------------------------------------------- #

def ggplot_scripts_for_all_plots script_requested
  puts "calling ggplot..."
  case script_requested

  when "peak_rank_raw_height_foldChange"
    return "
    ggplot(a) + geom_point(aes(x=rank,y=raw_height,color=FoldChange)) +
    xlab(\"peak rank\") +  
    ylab(\"summit raw height\")

    ggsave(\"#{$fplot_name}.pdf\")
    "

  when "nucleosome_wrap"
    ylab = $file_nuclhist_data.include?("bunnikEtAl2014") ? "Nucleosome value" : "Histone logFold change over input"
    #write_html_helper_nucleosome_wrap

    return "
    ggplot(a) + geom_ribbon(aes(x=i,ymin=zmin,ymax=zmax),alpha=0.3,fill=\"red\") + 
    geom_line(aes(x=i,y=zavg),color=\"black\") +
    xlab(\"#{2*$WINDOW_SIZE}b window around the peaks summits\") +  
    ylab(\"Z-score of #{ylab}\") +
    coord_cartesian(ylim = c(-1, 2)) + 
    facet_wrap(~stage) +
    ggtitle(\"#{$fplot_title}\") +
    theme(plot.title = element_text(hjust = 0.5))

    ggsave(\"#{$fplot_name}_znorm.jpeg\",width=19,height=7)
    "

  when "peaks_differentail_expression_plot_and_ttest"
    return "
    pval = t.test(a[a$cond == \"#{$cond1}\",]$expression_value,a[a$cond == \"#{$cond2}\",]$expression_value,paired = TRUE, alternative = \"two.sided\")$p.value
    
    ggplot(a) + geom_point(aes(x=raw_height,y=expression_value,color=cond)) + 
    facet_wrap(~cond) +
    ylim(c(0,0.003)) +
    xlab(\"summit raw height\") +
    ylab(\"Expression value\") +
    ggtitle(paste(\"lnc_#{$lnc} \\n (#{$temp_name}) \\n p_val =\",round(pval,5),sep=\"\")) +
    theme(plot.title = element_text(hjust = 0.5)) +
    theme(legend.position = \"none\")

    ggsave(\"#{$fplot_name}.jpeg\",width=12,height=7)
    "

  when "other"
    return "Bobby"

  else
    $DONT_RUN_GGPLOT = true
    puts "hey, no script found so run it on your own"
  end
end


def write_html_helper_nucleosome_wrap
  fo = File.open("#{$PATH}/Temp/Plots/#{$bedfile}_html_helper.txt", 'a')
  fo.puts "<img src=\"#{$fplot_name}_raw.jpeg\">"
  fo.puts "<img src=\"#{$fplot_name}_znorm.jpeg\">"
  fo.puts "<p></p>\n<hr></hr>\n"
  fo.close
end



# --------------------------------------------------------------------------- #
# Creates the basic wrapper around ggplot(a) and calls R to
# run the ggplot script if it has been automated.
# --------------------------------------------------------------------------- #
def run_ggplot_script script_requested
  $fo_ggplot = File.open("#{$PATH}/Temp/Plots/#{$fplot_name}_ggplot.r", 'w')
  $fo_ggplot.puts "library(ggplot2)"
  $fo_ggplot.puts "setwd(\"#{$PATH}/Temp/Plots/\")"
  $fo_ggplot.puts "a <- read.table(\"#{$fplot_name}.txt\",header=T)"

  $fo_ggplot.puts(ggplot_scripts_for_all_plots(script_requested))
  $fo_ggplot.close

  # run the ggplot script unless none was found
  `Rscript #{$PATH}/Temp/Plots/#{$fplot_name}_ggplot.r` unless $DONT_RUN_GGPLOT
end

