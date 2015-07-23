/*Macro read in all files with endinghistos.root,
search the tot_barcode histogram inside and move it 
to one common output file
*/


#include <list>


using namespace std;
void rewritehist(const char *dirname="./", const char *ext="histos.root")
{
   TH1F *tot_vs_th92 = new TH1F("tot_vs_th92","tot_vs_th92",200,0,200);
   TH1F *tot_vs_th96 = new TH1F("tot_vs_th96","tot_vs_th96",200,0,200);
   TH1F *tot_vs_th92_max = new TH1F("tot_vs_th92_max","tot_vs_th92_max",200,0,200);
   TH1F *tot_vs_th96_max = new TH1F("tot_vs_th96_max","tot_vs_th96_max",200,0,200);
   TH1F *tot_vs_th92_maxGaus = new TH1F("tot_vs_th92_maxGaus","tot_vs_th92_maxGaus",200,0,200);
   TH1F *tot_vs_th96_maxGaus = new TH1F("tot_vs_th96_maxGaus","tot_vs_th96_maxGaus",200,0,200);

   TFile* outputfile = TFile::Open("outcome.root", "RECREATE");  // my output file
   std::list<TString> mylist;
   TSystemDirectory dir(dirname, dirname);
   TList *files = dir.GetListOfFiles();
   if (files) {
      TSystemFile *file;
      TString fname;
      TIter next(files);
      while ((file=(TSystemFile*)next())) {
         fname = file->GetName();
         if (!file->IsDirectory() && fname.EndsWith(ext)) {
	    mylist.push_front(fname);
         }
      }
   }
	mylist->sort();
	//for (int k=0; k< mylist->GetSize(); k++)
	//	cout<<mylist[k]<<endl;
   for (std::list<TString>::iterator it=mylist.begin(); it!=mylist.end(); ++it)
   {   
      int bin =0;
      std::cout << ' ' << *it<<endl;
      TFile *flMC_file = new TFile(*it);
      TString title = (*it);
      title = title(14,3);
      if(title.IsDigit())
	bin = title.Atoi();   
        cout<<title<<"   bin:"<<bin<<endl;
      TH1F* tot92 = (TH1F*)flMC_file->Get("tot_hist_ch92");
      TH1F* tot96 = (TH1F*)flMC_file->Get("tot_hist_ch96");

      tot92->GetXaxis()->SetRangeUser(0,1000);
      tot96->GetXaxis()->SetRangeUser(0,1000);
//getting x position of maximal bin
      int binmax92 = tot92->GetMaximumBin();
      double x92 = tot92->GetXaxis()->GetBinCenter(binmax92);
      int binmax96 = tot96->GetMaximumBin();
      double x96 = tot96->GetXaxis()->GetBinCenter(binmax96);

//setting range for good fit
      tot92->GetXaxis()->SetRangeUser(x92-3, x92+3);
      tot96->GetXaxis()->SetRangeUser(x96-3, x96+3);
      tot92->Fit("gaus");
      tot96->Fit("gaus");



      TF1 *gaus92 = tot92->GetFunction("gaus");
      TF1 *gaus96 = tot96->GetFunction("gaus");
      if(gaus92 != NULL)
      {
	tot_vs_th92->SetBinContent(bin+1, gaus92->GetParameter(1));
	tot_vs_th92->SetBinError(bin+1, gaus92->GetParameter(2));//gaus92->GetParError(1));
      }
      else
      {
	tot_vs_th92->SetBinContent(bin+1, -10);
      }

      if(gaus96 != NULL)
      {
	tot_vs_th96->SetBinContent(bin+1, gaus96->GetParameter(1));
	tot_vs_th96->SetBinError(bin+1, gaus96->GetParameter(2));//gaus96->GetParError(1));
      }
      else 
      {
	tot_vs_th96->SetBinContent(bin+1, -10);
      }
      	tot_vs_th96_max->SetBinContent(bin+1, x96);
	tot_vs_th92_max->SetBinContent(bin+1, x92);

//      tot_vs_th92->SetBinContent(bin+1, tot92->GetMean());
//      tot_vs_th96->SetBinContent(bin+1, tot96->GetMean());
      TH2F* h1dMC_NN = (TH2F*)flMC_file->Get("tot_barcode");
      h1dMC_NN->SetTitle(title.Data());
      outputfile->cd();
      h1dMC_NN->Write();
      tot92->SetTitle(title.Data());
      tot96->SetTitle(title.Data());
      tot92->Write();
      tot96->Write();
      //flMC_file->GetList()Write(); //write in memory objects of 1st file to the current file
      flMC_file->cd();
      flMC_file->Close();

   }
    outputfile->cd(); 
    tot_vs_th92->Write();
    tot_vs_th96->Write();
    tot_vs_th92_max->Write();
    tot_vs_th96_max->Write();
    outputfile->Close();
}
