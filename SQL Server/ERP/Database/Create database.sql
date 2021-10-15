USE [master]
GO

/****** Object:  Database [ERP]    Script Date: 10/10/2021 14:51:55 ******/
CREATE DATABASE [ERP]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'ERP', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\ERP.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'ERP_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL15.SQLEXPRESS\MSSQL\DATA\ERP_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT
GO

IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [ERP].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO

ALTER DATABASE [ERP] SET ANSI_NULL_DEFAULT OFF 
GO

ALTER DATABASE [ERP] SET ANSI_NULLS OFF 
GO

ALTER DATABASE [ERP] SET ANSI_PADDING OFF 
GO

ALTER DATABASE [ERP] SET ANSI_WARNINGS OFF 
GO

ALTER DATABASE [ERP] SET ARITHABORT OFF 
GO

ALTER DATABASE [ERP] SET AUTO_CLOSE OFF 
GO

ALTER DATABASE [ERP] SET AUTO_SHRINK OFF 
GO

ALTER DATABASE [ERP] SET AUTO_UPDATE_STATISTICS ON 
GO

ALTER DATABASE [ERP] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO

ALTER DATABASE [ERP] SET CURSOR_DEFAULT  GLOBAL 
GO

ALTER DATABASE [ERP] SET CONCAT_NULL_YIELDS_NULL OFF 
GO

ALTER DATABASE [ERP] SET NUMERIC_ROUNDABORT OFF 
GO

ALTER DATABASE [ERP] SET QUOTED_IDENTIFIER OFF 
GO

ALTER DATABASE [ERP] SET RECURSIVE_TRIGGERS OFF 
GO

ALTER DATABASE [ERP] SET  DISABLE_BROKER 
GO

ALTER DATABASE [ERP] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO

ALTER DATABASE [ERP] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO

ALTER DATABASE [ERP] SET TRUSTWORTHY OFF 
GO

ALTER DATABASE [ERP] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO

ALTER DATABASE [ERP] SET PARAMETERIZATION SIMPLE 
GO

ALTER DATABASE [ERP] SET READ_COMMITTED_SNAPSHOT OFF 
GO

ALTER DATABASE [ERP] SET HONOR_BROKER_PRIORITY OFF 
GO

ALTER DATABASE [ERP] SET RECOVERY SIMPLE 
GO

ALTER DATABASE [ERP] SET  MULTI_USER 
GO

ALTER DATABASE [ERP] SET PAGE_VERIFY CHECKSUM  
GO

ALTER DATABASE [ERP] SET DB_CHAINING OFF 
GO

ALTER DATABASE [ERP] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO

ALTER DATABASE [ERP] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO

ALTER DATABASE [ERP] SET DELAYED_DURABILITY = DISABLED 
GO

ALTER DATABASE [ERP] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO

ALTER DATABASE [ERP] SET QUERY_STORE = OFF
GO

ALTER DATABASE [ERP] SET  READ_WRITE 
GO
